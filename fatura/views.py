from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from cari.models import *
from stok.models import *
from siparis.models import *
from irsaliye.models import *
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
#tarih = time.strftime("%Y-%m-%d")
#saat = time.strftime("%H:%M")
#suan = tarih+" "+saat
suan = timezone.now()

def FaturaOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsFatura == True):
			islemlerKontrol = get_object_or_404(FaturaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsFaturaOlustur == True):
				if request.is_ajax():
					ajaxSil = request.POST.get("ajaxSil")
					if ajaxSil:
						ajaxFaturaHareketleri = get_object_or_404(FaturaHareketleri, id=ajaxSil)
						ajaxFaturaHareketleri.delete()
						context = {"ajaxMesaj": "Silme İşlemi Başarılı!",}
						return JsonResponse(context)	

					ajaxFaturaTipiKontrol = request.POST.get("ajaxFaturaTipiKontrol")
					if ajaxFaturaTipiKontrol:
						try:
							sqlFaturaNo = get_object_or_404(FaturaNo,id="1")
							varFaturaSeri = sqlFaturaNo.FaturaSeri
							varFaturaSira = sqlFaturaNo.FaturaSira
						except:
							varFaturaSeri = ""
							varFaturaSira = ""
						context = {
							"ajaxFaturaSeri": varFaturaSeri,
						    "ajaxFaturaSira": varFaturaSira,
						}	
						return JsonResponse(context)
						
					ajaxStok       = request.POST.get("ajaxStok")
					ajaxFatTipStok = request.POST.get("ajaxFatTipStok")
					if ajaxStok:
						sqlStok = get_object_or_404(Stok, StokKodu=ajaxStok)
						birimFiyati = ""
						if(ajaxFatTipStok == "1"):
							birimFiyati = sqlStok.SatisFiyati
						if(ajaxFatTipStok == "2"):
							birimFiyati = sqlStok.AlisFiyati
						context = {
							"birimFiyati"     : str(birimFiyati),
					        "sqlStokKdvOrani" : str(sqlStok.KdvOrani),
					        "sqlStokNitelik"  : str(sqlStok.StokNitelik),
						}	
						return JsonResponse(context)

					ajaxMiktarKontrol = request.POST.get("ajaxMiktarKontrol")
					ajaxStokKodu      = request.POST.get("ajaxStokKodu")
					if(ajaxMiktarKontrol):
						sqlStokMiktarControl = get_object_or_404(Stok, StokKodu=ajaxStokKodu)
						if(int(sqlStokMiktarControl.StokMiktar) - int(ajaxMiktarKontrol) < 0):
							context = {"ajaxMesaj" : "1",}
						else:
							context = {"ajaxMesaj" : "",}
						return JsonResponse(context)

					ajaxFaturaSeri  = request.POST.get("ajaxFaturaSeri")
					ajaxFaturaSira  = request.POST.get("ajaxFaturaSira")
					ajaxFaturaTipi  = request.POST.get("ajaxFaturaTipi")
					ajaxStokKodu    = request.POST.get("ajaxStokKodu")
					ajaxStokNitelik = request.POST.get("ajaxNitelik")
					ajaxMiktar      = request.POST.get("ajaxMiktar")
					ajaxBirimFiyat  = request.POST.get("ajaxBirimFiyat")
					ajaxIskOrani    = request.POST.get("ajaxIskontoOrani")
					ajaxKdvOrani    = request.POST.get("ajaxKdvOrani")
					if(ajaxStokKodu != None):
						if(ajaxFaturaSeri and ajaxFaturaSira and ajaxFaturaTipi and ajaxStokKodu and ajaxStokNitelik and ajaxMiktar and ajaxBirimFiyat and ajaxIskOrani and ajaxKdvOrani):
							sqlFaturaHareketleri = FaturaHareketleri()
							sqlFaturaHareketleri.FaturaSeri   = ajaxFaturaSeri
							sqlFaturaHareketleri.FaturaSira   = ajaxFaturaSira
							sqlFaturaHareketleri.StokKodu     = ajaxStokKodu
							sqlFaturaHareketleri.Nitelik      = ajaxStokNitelik
							sqlFaturaHareketleri.Miktar       = ajaxMiktar
							sqlFaturaHareketleri.BirimFiyat   = ajaxBirimFiyat
							sqlFaturaHareketleri.IskontoOrani = ajaxIskOrani
							sqlFaturaHareketleri.KdvOrani     = ajaxKdvOrani
							sqlFaturaHareketleri.save()	
							sqlStok = get_object_or_404(Stok, StokKodu=ajaxStokKodu)
							context = {
								"ajaxMesaj"       : "1",
								"sqlId"           : sqlFaturaHareketleri.id, 
						        "sqlStokKodu"     : sqlStok.StokAdi,
						        "sqlFaturaSeri"   : sqlFaturaHareketleri.FaturaSeri,
						        "sqlFaturaSira"   : sqlFaturaHareketleri.FaturaSira,
						        "sqlNitelik"      : sqlFaturaHareketleri.Nitelik,
								"sqlMiktar"       : str(sqlFaturaHareketleri.Miktar),
								"sqlBirimFiyat"   : str(sqlFaturaHareketleri.BirimFiyat),
								"sqlIskontoOrani" : str(sqlFaturaHareketleri.IskontoOrani),
								"sqlKdvOrani"     : str(sqlFaturaHareketleri.KdvOrani),
							}
							return JsonResponse(context)
						else:
							context = {"ajaxMesaj" : "Lütfen Formu Boş Bırakmayınız !"}
							return JsonResponse(context)	

					ajaxKey 			   = request.POST.get("ajaxKey")
					ajaxKey1 			   = request.POST.get("ajaxKey1")
					ajaxKey2 			   = request.POST.get("ajaxKey2")
					cariKoduSave		   = request.POST.get("ajaxCariKodu")
					faturaSeriSave 		   = request.POST.get("ajaxFaturaSeri")
					faturaSiraSave 		   = request.POST.get("ajaxFaturaSira")
					faturaTipiSave 		   = request.POST.get("ajaxFaturaTipi")
					ajaxIslemTarihi 	   = request.POST.get("ajaxIslemTarihi")
					toplamBrutTutarSave    = request.POST.get("ajaxToplamBrutTutar")
					toplamKdvSave 		   = request.POST.get("ajaxToplamKdv")
					toplamBrutTutarReplace = toplamBrutTutarSave.replace(",",".")
					toplamKdvTutarReplace  = toplamKdvSave.replace(",",".")					
					if (cariKoduSave and faturaSeriSave and faturaSiraSave and faturaTipiSave and ajaxIslemTarihi and toplamBrutTutarSave and toplamKdvSave):
						if(ajaxKey == "0"):	
							faturaSave = Fatura()
							faturaSave.CariKodu        = cariKoduSave
							faturaSave.KullaniciKodu   = request.session["KullaniciKodu"]
							faturaSave.FaturaSeri      = faturaSeriSave
							faturaSave.FaturaSira      = int(faturaSiraSave)
							faturaSave.FaturaTipi      = faturaTipiSave
							faturaSave.IslemTarihi     = ajaxIslemTarihi
							faturaSave.ToplamBrutTutar = float(toplamBrutTutarReplace)
							faturaSave.ToplamKdv       = float(toplamKdvTutarReplace)
							if(faturaTipiSave == "2"):
								faturaSave.IsTransferCache = True
							faturaSave.save()
							if(faturaTipiSave == "1"):
								try:
									sqlFaturaNoGuncelle = get_object_or_404(FaturaNo,id="1")
									sqlFaturaNoGuncelle.FaturaSeri = faturaSeriSave
									sqlFaturaNoGuncelle.FaturaSira = int(faturaSiraSave) + 1
									sqlFaturaNoGuncelle.save()
								except:
									pass
							sqlFaturaHareketleri = FaturaHareketleri.objects.filter(FaturaSeri=faturaSave.FaturaSeri,FaturaSira=faturaSave.FaturaSira)	
							for faturaHareketleri in sqlFaturaHareketleri:
								faturaHareketleri.IsSaved    = True
								faturaHareketleri.save()
								sqlStok = get_object_or_404(Stok, StokKodu=faturaHareketleri.StokKodu)
								if(faturaTipiSave == "1"):
									sqlStok.StokMiktar = int(sqlStok.StokMiktar) - int(faturaHareketleri.Miktar)
									sqlStok.save()
									stokHareketleri = StokHareketleri()
									stokHareketleri.StokAdi               = sqlStok.StokAdi
									stokHareketleri.StokKodu              = faturaHareketleri.StokKodu
									stokHareketleri.StokNitelik           = faturaHareketleri.Nitelik
									stokHareketleri.StokMiktar            = faturaHareketleri.Miktar
									stokHareketleri.SatisFiyati           = faturaHareketleri.BirimFiyat
									stokHareketleri.SonIskontoOrani       = faturaHareketleri.IskontoOrani
									stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
									stokHareketleri.StokHareketTarihi     = suan
									stokHareketleri.save()
								if(faturaTipiSave == "2"):
									sqlStok.StokMiktar = int(sqlStok.StokMiktar) + int(faturaHareketleri.Miktar)
									sqlStok.save()
									stokHareketleri = StokHareketleri()
									stokHareketleri.StokAdi               = sqlStok.StokAdi
									stokHareketleri.StokKodu              = faturaHareketleri.StokKodu
									stokHareketleri.StokNitelik           = faturaHareketleri.Nitelik
									stokHareketleri.StokMiktar            = faturaHareketleri.Miktar
									stokHareketleri.AlisFiyati            = faturaHareketleri.BirimFiyat
									stokHareketleri.SonIskontoOrani       = faturaHareketleri.IskontoOrani
									stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
									stokHareketleri.StokHareketTarihi     = suan 
									stokHareketleri.save()	
						if(ajaxKey == "1"):
							faturaSave = Fatura()
							faturaSave.CariKodu        = cariKoduSave
							faturaSave.KullaniciKodu   = request.session["KullaniciKodu"]
							faturaSave.FaturaSeri      = faturaSeriSave
							faturaSave.FaturaSira      = int(faturaSiraSave)
							faturaSave.FaturaTipi      = faturaTipiSave
							faturaSave.IslemTarihi     = ajaxIslemTarihi
							faturaSave.ToplamBrutTutar = float(toplamBrutTutarReplace)
							faturaSave.ToplamKdv       = float(toplamKdvTutarReplace)
							if(faturaTipiSave == "2"):
								faturaSave.IsTransferCache = True
							faturaSave.save()
							if(faturaTipiSave == "1"):
								try:
									sqlFaturaNoGuncelle = get_object_or_404(FaturaNo,id="1")
									sqlFaturaNoGuncelle.FaturaSeri = faturaSeriSave
									sqlFaturaNoGuncelle.FaturaSira = int(faturaSiraSave) + 1
									sqlFaturaNoGuncelle.save()
								except:
									pass

							siparisTipi = ""
							if(faturaTipiSave == "1"):
								siparisTipi = "2"
							if(faturaTipiSave == "2"):
								siparisTipi = "1"	
							sqlSiparisFatura = get_object_or_404(Siparis,SiparisFisiNo=ajaxKey1,SiparisTipi=siparisTipi,IsCanceled=False)
							sqlSiparisFatura.IsVerified = True
							sqlSiparisFatura.save()

							sqlSiparisHareketleriFatura = SiparisHareketleri.objects.filter(SiparisFisiNo=ajaxKey1,SiparisTipi=siparisTipi)
							for siparisHareketleriFatura in sqlSiparisHareketleriFatura:
								siparisHareketleriFatura.IsVerified = True
								siparisHareketleriFatura.save()
								faturaHareketleriFatura = FaturaHareketleri()
								faturaHareketleriFatura.FaturaSeri   = faturaSeriSave
								faturaHareketleriFatura.FaturaSira   = faturaSiraSave
								faturaHareketleriFatura.StokKodu     = siparisHareketleriFatura.StokKodu
								faturaHareketleriFatura.Nitelik      = siparisHareketleriFatura.Nitelik
								faturaHareketleriFatura.Miktar       = siparisHareketleriFatura.Miktar
								faturaHareketleriFatura.BirimFiyat   = siparisHareketleriFatura.BirimFiyat
								faturaHareketleriFatura.IskontoOrani = siparisHareketleriFatura.IskontoOrani
								faturaHareketleriFatura.KdvOrani     = siparisHareketleriFatura.KdvOrani
								faturaHareketleriFatura.IsSaved      = True
								faturaHareketleriFatura.save()

								sqlStok = get_object_or_404(Stok, StokKodu=siparisHareketleriFatura.StokKodu)
								if(faturaTipiSave == "1"):
									sqlStok.StokMiktar = int(sqlStok.StokMiktar) - int(siparisHareketleriFatura.Miktar)
									sqlStok.save()
									stokHareketleri = StokHareketleri()
									stokHareketleri.StokAdi               = sqlStok.StokAdi
									stokHareketleri.StokKodu              = siparisHareketleriFatura.StokKodu
									stokHareketleri.StokNitelik           = siparisHareketleriFatura.Nitelik
									stokHareketleri.StokMiktar            = siparisHareketleriFatura.Miktar
									stokHareketleri.SatisFiyati           = siparisHareketleriFatura.BirimFiyat
									stokHareketleri.SonIskontoOrani       = siparisHareketleriFatura.IskontoOrani
									stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
									stokHareketleri.StokHareketTarihi     = suan
									stokHareketleri.save()
								if(faturaTipiSave == "2"):
									sqlStok.StokMiktar = int(sqlStok.StokMiktar) + int(siparisHareketleriFatura.Miktar)
									sqlStok.save()
									stokHareketleri = StokHareketleri()
									stokHareketleri.StokAdi               = sqlStok.StokAdi
									stokHareketleri.StokKodu              = siparisHareketleriFatura.StokKodu
									stokHareketleri.StokNitelik           = siparisHareketleriFatura.Nitelik
									stokHareketleri.StokMiktar            = siparisHareketleriFatura.Miktar
									stokHareketleri.AlisFiyati            = siparisHareketleriFatura.BirimFiyat
									stokHareketleri.SonIskontoOrani       = siparisHareketleriFatura.IskontoOrani
									stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
									stokHareketleri.StokHareketTarihi     = suan 
									stokHareketleri.save()
						if(ajaxKey == "2"):
							faturaSave = Fatura()
							faturaSave.CariKodu        = cariKoduSave
							faturaSave.KullaniciKodu   = request.session["KullaniciKodu"]
							faturaSave.FaturaSeri      = faturaSeriSave
							faturaSave.FaturaSira      = int(faturaSiraSave)
							faturaSave.FaturaTipi      = faturaTipiSave
							faturaSave.ToplamBrutTutar = float(toplamBrutTutarReplace)
							faturaSave.ToplamKdv       = float(toplamKdvTutarReplace)
							faturaSave.IslemTarihi     = ajaxIslemTarihi
							faturaSave.IsTransferCache = True
							if(faturaTipiSave == "2"):
								faturaSave.IsTransferCache = True
							faturaSave.save()
							if(faturaTipiSave == "1"):
								try:
									sqlFaturaNoGuncelle = get_object_or_404(FaturaNo,id="1")
									sqlFaturaNoGuncelle.FaturaSeri = faturaSeriSave
									sqlFaturaNoGuncelle.FaturaSira = int(faturaSiraSave) + 1
									sqlFaturaNoGuncelle.save()
								except:
									pass
							for faturaHareketleriIsTransferCache in FaturaHareketleri.objects.filter(FaturaSeri=faturaSave.FaturaSeri,FaturaSira=faturaSave.FaturaSira):
								faturaHareketleriIsTransferCache.IsTransferCache = True
								faturaHareketleriIsTransferCache.save()
							sqlIrsaliyeFatura = get_object_or_404(Irsaliye,IrsaliyeNo=ajaxKey2,IrsaliyeTipi=faturaTipiSave,IsCanceled=False)
							sqlIrsaliyeFatura.IsVerified = True
							sqlIrsaliyeFatura.save()
							sqlIrsaliyeHareketleriFatura = IrsaliyeHareketleri.objects.filter(IrsaliyeNo=ajaxKey2,IrsaliyeTipi=faturaTipiSave)
							for irsaliyeHareketleriFatura in sqlIrsaliyeHareketleriFatura:
								irsaliyeHareketleriFatura.IsVerified = True
								irsaliyeHareketleriFatura.save()
								faturaHareketleriFatura = FaturaHareketleri()
								faturaHareketleriFatura.FaturaSeri   = faturaSeriSave
								faturaHareketleriFatura.FaturaSira   = faturaSiraSave
								faturaHareketleriFatura.StokKodu     = irsaliyeHareketleriFatura.StokKodu
								faturaHareketleriFatura.Nitelik      = irsaliyeHareketleriFatura.Nitelik
								faturaHareketleriFatura.Miktar       = irsaliyeHareketleriFatura.Miktar
								faturaHareketleriFatura.BirimFiyat   = irsaliyeHareketleriFatura.BirimFiyat
								faturaHareketleriFatura.IskontoOrani = irsaliyeHareketleriFatura.IskontoOrani
								faturaHareketleriFatura.KdvOrani     = irsaliyeHareketleriFatura.KdvOrani
								faturaHareketleriFatura.IsSaved      = True
								faturaHareketleriFatura.save()

								sqlStok = get_object_or_404(Stok, StokKodu=irsaliyeHareketleriFatura.StokKodu)
								if(faturaTipiSave == "1"):
									sqlStok.StokMiktar = int(sqlStok.StokMiktar) - int(irsaliyeHareketleriFatura.Miktar)
									sqlStok.save()
									stokHareketleri = StokHareketleri()
									stokHareketleri.StokAdi               = sqlStok.StokAdi
									stokHareketleri.StokKodu              = irsaliyeHareketleriFatura.StokKodu
									stokHareketleri.StokNitelik           = irsaliyeHareketleriFatura.Nitelik
									stokHareketleri.StokMiktar            = irsaliyeHareketleriFatura.Miktar
									stokHareketleri.SatisFiyati           = irsaliyeHareketleriFatura.BirimFiyat
									stokHareketleri.SonIskontoOrani       = irsaliyeHareketleriFatura.IskontoOrani
									stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
									stokHareketleri.StokHareketTarihi     = suan
									stokHareketleri.save()
								if(faturaTipiSave == "2"):
									sqlStok.StokMiktar = int(sqlStok.StokMiktar) + int(irsaliyeHareketleriFatura.Miktar)
									sqlStok.save()
									stokHareketleri = StokHareketleri()
									stokHareketleri.StokAdi               = sqlStok.StokAdi
									stokHareketleri.StokKodu              = irsaliyeHareketleriFatura.StokKodu
									stokHareketleri.StokNitelik           = irsaliyeHareketleriFatura.Nitelik
									stokHareketleri.StokMiktar            = irsaliyeHareketleriFatura.Miktar
									stokHareketleri.AlisFiyati            = irsaliyeHareketleriFatura.BirimFiyat
									stokHareketleri.SonIskontoOrani       = irsaliyeHareketleriFatura.IskontoOrani
									stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
									stokHareketleri.StokHareketTarihi     = suan 
									stokHareketleri.save()
						context = {"ajaxMesaj" : "1",}
						return JsonResponse(context)
					else:
						context = {"ajaxMesaj" : "Lütfen Formu Boş Bırakmayınız !",}		
						return JsonResponse(context)			
				#Siparis Yada İrsaliye Form Doldurma
				key = "0"
				try:
					sqlSiparis = get_object_or_404(Siparis,IsTransferred=True)
					sqlSiparisHareketleri = SiparisHareketleri.objects.filter(SiparisFisiNo=sqlSiparis.SiparisFisiNo,SiparisTipi=sqlSiparis.SiparisTipi,IsCanceled=False)
					sqlCariSiparis = get_object_or_404(Cari,CariKodu=sqlSiparis.CariKodu)
					sqlCariIrtibatSiparis = get_object_or_404(CariIrtibat,CariKodu=sqlCariSiparis.CariKodu)
					varOdenecekTutar = float(sqlSiparis.ToplamBrutTutar) + float(sqlSiparis.ToplamKdv)
					varFaturaTipi = ""
					if(sqlSiparis.SiparisTipi == "1"):
						varFaturaTipi = "2"
					if(sqlSiparis.SiparisTipi == "2"):
						varFaturaTipi = "1"
					if(sqlSiparis.SiparisTipi == "2"):
						try:
							sqlFaturaTipiSiparis = get_object_or_404(FaturaNo,id="1")
							varFaturaSeriSiparis = sqlFaturaTipiSiparis.FaturaSeri
							varFaturaSiraSiparis = sqlFaturaTipiSiparis.FaturaSira
						except:
							varFaturaSeriSiparis = ""
							varFaturaSiraSiparis = ""
					else:
						varFaturaSeriSiparis = ""
						varFaturaSiraSiparis = ""
					key = "1"	
				except:
					varOdenecekTutar      = ""
					varFaturaSeriSiparis  = ""
					varFaturaSiraSiparis  = ""
					sqlCariSiparis        = ""
					sqlCariIrtibatSiparis = ""
					sqlSiparis            = ""
					sqlSiparisHareketleri = ""	
				try:
					sqlIrsaliye = get_object_or_404(Irsaliye,IsTransferred=True)
					sqlIrsaliyeHareketleri = IrsaliyeHareketleri.objects.filter(IrsaliyeNo=sqlIrsaliye.IrsaliyeNo,IrsaliyeTipi=sqlIrsaliye.IrsaliyeTipi,IsCanceled=False)
					sqlCariIrsaliye = get_object_or_404(Cari,CariKodu=sqlIrsaliye.CariKodu)
					sqlCariIrtibatIrsaliye = get_object_or_404(CariIrtibat,CariKodu=sqlCariIrsaliye.CariKodu)
					varOdenecekTutarIrsaliye = float(sqlIrsaliye.ToplamBrutTutar) + float(sqlIrsaliye.ToplamKdv)
					varIrsaliyeTipi = ""
					if(sqlIrsaliye.IrsaliyeTipi == "1"):
						varIrsaliyeTipi = "1"
					if(sqlIrsaliye.IrsaliyeTipi == "2"):
						varIrsaliyeTipi = "2"
					if(sqlIrsaliye.IrsaliyeTipi == "1"):
						try:
							sqlFaturaTipiIrsaliye = get_object_or_404(FaturaNo,id="1")
							varFaturaSeriIrsaliye = sqlFaturaTipiIrsaliye.FaturaSeri
							varFaturaSiraIrsaliye = sqlFaturaTipiIrsaliye.FaturaSira
						except:
							varFaturaSeriIrsaliye = ""
							varFaturaSiraIrsaliye = ""
					else:
						varFaturaSeriIrsaliye = ""
						varFaturaSiraIrsaliye = ""
					key = "2"		
				except:
					varOdenecekTutarIrsaliye = ""
					varFaturaSeriIrsaliye    = ""
					varFaturaSiraIrsaliye    = ""
					sqlCariIrsaliye          = ""
					sqlCariIrtibatIrsaliye   = ""
					sqlIrsaliye              = ""
					sqlIrsaliyeHareketleri   = ""
				#Siparis Yada İrsaliye Form Doldurma
				#Siparis Yada İrsaliye Transfer Olupta Faturası Oluşturulmayan İşlemlerin
				#Transferinin İptali			
				try:
					for siparisIsTransferred in Siparis.objects.filter(IsTransferred=True):
						siparisIsTransferred.IsTransferred = False
						siparisIsTransferred.save()
					for siparisHareketleriIsTransferred in SiparisHareketleri.objects.filter(IsSaved=True,IsTransferred=True):
						siparisHareketleriIsTransferred.IsTransferred = False
						siparisHareketleriIsTransferred.save()	
				except:
					pass
				try:
					for irsaliyeIsTransferred in Irsaliye.objects.filter(IsTransferred=True):
						irsaliyeIsTransferred.IsTransferred = False
						irsaliyeIsTransferred.save()
					for irsaliyeHareketleriIsTransferred in IrsaliyeHareketleri.objects.filter(IsSaved=True,IsTransferred=True):
						irsaliyeHareketleriIsTransferred.IsTransferred = False
						irsaliyeHareketleriIsTransferred.save()	
				except:
					pass
				sqlStok = Stok.objects.filter(IsDeleted=False)
				sqlCari = Cari.objects.filter(IsDeleted=False)
				sqlFaturaHareketleriFilter = FaturaHareketleri.objects.filter(IsSaved=False)
				context = {
					"modulYetkisi" 	   			 : modulYetkisi,
					"suan" 						 : suan,
					"key"       				 : key,
					"varOdenecekTutar"           : varOdenecekTutar,
					"varOdenecekTutarIrsaliye"   : varOdenecekTutarIrsaliye,
					"varFaturaSeriSiparis"       : varFaturaSeriSiparis,
					"varFaturaSiraSiparis"       : varFaturaSiraSiparis,
					"varFaturaSeriIrsaliye"      : varFaturaSeriIrsaliye,
					"varFaturaSiraIrsaliye"      : varFaturaSiraIrsaliye,
					"sqlCariSiparis"             : sqlCariSiparis,
					"sqlCariIrtibatSiparis"      : sqlCariIrtibatSiparis,
					"sqlCariIrsaliye"            : sqlCariIrsaliye,
					"sqlCariIrtibatIrsaliye"     : sqlCariIrtibatIrsaliye,
					"sqlSiparis"                 : sqlSiparis,
					"sqlSiparisHareketleri"      : sqlSiparisHareketleri,
					"sqlIrsaliye"                : sqlIrsaliye,
					"sqlIrsaliyeHareketleri"     : sqlIrsaliyeHareketleri,
					"sqlStok"              		 : sqlStok,
					"sqlCari"            		 : sqlCari,
					"sqlFaturaHareketleriFilter" : sqlFaturaHareketleriFilter,
				}
				if(key == "0"):
					return render (request, "fatura/olustur.html", context)
				if(key == "1"):
					return render (request, "fatura/olusturSiparis.html", context)
				if(key == "2"):
					return render (request, "fatura/olusturIrsaliye.html", context)		
			else:		
				messages.success(request, "Fatura Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def FaturaListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsFatura == True):
			islemlerKontrol = get_object_or_404(FaturaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsFaturaListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlFaturaDetay = get_object_or_404(Fatura, id=ajaxDetay)
						sqlFaturaHarDetay = FaturaHareketleri.objects.filter(FaturaSeri=sqlFaturaDetay.FaturaSeri, FaturaSira=sqlFaturaDetay.FaturaSira)
						faturaHareketleriList = []	
						for faturaHarDetay in sqlFaturaHarDetay:
							faturaHareketleriDetayList = [faturaHarDetay.StokKodu,faturaHarDetay.Miktar,faturaHarDetay.Nitelik,\
							faturaHarDetay.BirimFiyat,faturaHarDetay.IskontoOrani,faturaHarDetay.KdvOrani]
							faturaHareketleriList.append(faturaHareketleriDetayList)
						sqlStokDetay = get_object_or_404(Stok, StokKodu=faturaHarDetay.StokKodu)
						sqlCariDetay = get_object_or_404(Cari, CariKodu=sqlFaturaDetay.CariKodu)
						sqlCariIrtibatDetay = get_object_or_404(CariIrtibat, CariKodu=sqlCariDetay.CariKodu)	
						if(sqlFaturaDetay.FaturaTipi == "1"):
							varFaturaTipi = "Satış Faturası"
						elif(sqlFaturaDetay.FaturaTipi == "2"):
							varFaturaTipi = "Alış Faturası"	
						context = {
							"faturaHareketleriList"   : faturaHareketleriList,
							"ajaxFaturaSeri"       	  : sqlFaturaDetay.FaturaSeri,
							"ajaxFaturaSira"          : sqlFaturaDetay.FaturaSira,
							"ajaxFaturaTipi"          : varFaturaTipi,
							"ajaxIslemTarihi" 		  : sqlFaturaDetay.IslemTarihi,
							"ajaxToplamBrutTutar"     : sqlFaturaDetay.ToplamBrutTutar,
							"ajaxToplamKdv"           : sqlFaturaDetay.ToplamKdv,
							"ajaxCariUnvani"          : sqlCariDetay.CariUnvani,
							"ajaxVergiDairesi"        : sqlCariDetay.VergiDairesi,
							"ajaxVergiNumarasi"       : sqlCariDetay.VergiNumarasi,
							"ajaxAdres"               : sqlCariIrtibatDetay.Adres,
							"ajaxIl"                  : sqlCariIrtibatDetay.Il,
							"ajaxIlce"                : sqlCariIrtibatDetay.Ilce,
							"ajaxTel1"                : sqlCariIrtibatDetay.Tel1,
						}
						return JsonResponse(context)

					value1 = request.POST.get("ajaxFaturaSeriIptal")
					value2 = request.POST.get("ajaxFaturaSiraIptal")
					if(value1):
						valueIsCanceled = get_object_or_404(Fatura, FaturaSeri=value1, FaturaSira=value2)
						valueIsCanceled.IsCanceled = True
						valueIsCanceled.save()
						for faturaHareketleri in FaturaHareketleri.objects.filter(FaturaSeri=value1, FaturaSira=value2):
							faturaHareketleri.IsCanceled = True
							faturaHareketleri.save()
							sqlStok = get_object_or_404(Stok, StokKodu=faturaHareketleri.StokKodu)
							if(valueIsCanceled.FaturaTipi == "1"):
								sqlStok.StokMiktar = int(sqlStok.StokMiktar) + int(faturaHareketleri.Miktar)
								sqlStok.save()
								stokHareketleri = StokHareketleri()
								stokHareketleri.StokAdi               = sqlStok.StokAdi
								stokHareketleri.StokKodu              = faturaHareketleri.StokKodu
								stokHareketleri.StokNitelik           = faturaHareketleri.Nitelik
								stokHareketleri.StokMiktar            = faturaHareketleri.Miktar
								stokHareketleri.SatisFiyati           = faturaHareketleri.BirimFiyat
								stokHareketleri.SonIskontoOrani       = faturaHareketleri.IskontoOrani
								stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
								stokHareketleri.StokHareketTarihi     = suan
								stokHareketleri.IsCanceled            = True
								stokHareketleri.save()
							if(valueIsCanceled.FaturaTipi == "2"):
								sqlStok.StokMiktar = int(sqlStok.StokMiktar) - int(faturaHareketleri.Miktar)
								sqlStok.save()
								stokHareketleri = StokHareketleri()
								stokHareketleri.StokAdi               = sqlStok.StokAdi
								stokHareketleri.StokKodu              = faturaHareketleri.StokKodu
								stokHareketleri.StokNitelik           = faturaHareketleri.Nitelik
								stokHareketleri.StokMiktar            = faturaHareketleri.Miktar
								stokHareketleri.AlisFiyati            = faturaHareketleri.BirimFiyat
								stokHareketleri.SonIskontoOrani       = faturaHareketleri.IskontoOrani
								stokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
								stokHareketleri.StokHareketTarihi     = suan
								stokHareketleri.IsCanceled            = True
								stokHareketleri.save()
						context = {"ajaxMesaj" : "Başarılı",}	
						return JsonResponse(context)

					ajaxFaturaSeriSil = request.POST.get("ajaxFaturaSeriSil")
					ajaxFaturaSiraSil = request.POST.get("ajaxFaturaSiraSil")
					if(ajaxFaturaSeriSil):
						valueIsDeleted = get_object_or_404(Fatura, FaturaSeri=ajaxFaturaSeriSil, FaturaSira=ajaxFaturaSiraSil)
						valueIsDeleted.IsDeleted = True
						valueIsDeleted.save()
						for faturaHareketleri in FaturaHareketleri.objects.filter(FaturaSeri=ajaxFaturaSeriSil, FaturaSira=ajaxFaturaSiraSil):
							faturaHareketleri.IsDeleted = True
							faturaHareketleri.save()
						context = {"ajaxMesaj" : "Başarılı",}	
						return JsonResponse(context)	

					ajaxFaturaSeriIrsaliye = request.POST.get("ajaxFaturaSeriIrsaliye")
					ajaxFaturaSiraIrsaliye = request.POST.get("ajaxFaturaSiraIrsaliye")
					if(ajaxFaturaSeriIrsaliye and ajaxFaturaSiraIrsaliye != ""):
						faturaIsTransferred = get_object_or_404(Fatura, FaturaSeri=ajaxFaturaSeriIrsaliye, FaturaSira=ajaxFaturaSiraIrsaliye)
						faturaIsTransferred.IsTransferred = True
						faturaIsTransferred.save()
						for faturaHareketleriIsTransferred in FaturaHareketleri.objects.filter(FaturaSeri=ajaxFaturaSeriIrsaliye, FaturaSira=ajaxFaturaSiraIrsaliye):
							faturaHareketleriIsTransferred.IsTransferred = True
							faturaHareketleriIsTransferred.save()
						context = {"ajaxMesaj" : "Başarılı",}
						return JsonResponse(context)

				sqlFatura = Fatura.objects.filter(IsCanceled=False)
				sqlFaturaIsCanceled = Fatura.objects.filter(IsCanceled=True,IsDeleted=False)
				context = {
					"modulYetkisi" 	      : modulYetkisi,
					"islemlerKontrol"     : islemlerKontrol,
					"sqlFatura"           : sqlFatura,
					"sqlFaturaIsCanceled" : sqlFaturaIsCanceled,
				}
				return render (request, "fatura/listele.html", context)
			else:		
				messages.success(request, "Fatura Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def Tanimlamalar(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsFatura == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsFaturaTanimlamalari == True):
				ajaxFaturaSeri = request.POST.get("ajaxFaturaSeri")
				ajaxFaturaSira = request.POST.get("ajaxFaturaSira")
				try:
					sqlFaturaNo = get_object_or_404(FaturaNo,id="1")
					if request.is_ajax():
						sqlFaturaNo.FaturaSeri = ajaxFaturaSeri
						sqlFaturaNo.FaturaSira = ajaxFaturaSira
						sqlFaturaNo.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)
				except:
					if request.is_ajax():
						sqlFaturaNoOlustur = FaturaNo()
						sqlFaturaNoOlustur.FaturaSeri = ajaxFaturaSeri
						sqlFaturaNoOlustur.FaturaSira = ajaxFaturaSira
						sqlFaturaNoOlustur.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)
					sqlFaturaNo = ""
				context = {
					"modulYetkisi" : modulYetkisi,
					"sqlFaturaNo"  : sqlFaturaNo,
				}		
				return render (request, "fatura/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")