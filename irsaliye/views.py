from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from fatura.models import *
from cari.models import *
from stok.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

suan = timezone.now()

def IrsaliyeOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsIrsaliye == True):
			islemlerKontrol = get_object_or_404(IrsaliyeYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsIrsaliyeOlustur == True):
				if request.is_ajax():
					ajaxSil = request.POST.get("ajaxSil")
					if ajaxSil:
						sqlIrsaliyeHareketleri = get_object_or_404(IrsaliyeHareketleri, id=ajaxSil)	
						sqlIrsaliyeHareketleri.delete()
						context = {"ajaxMesaj": "Silme İşlemi Başarılı!",}
						return JsonResponse(context)

					ajaxIrsaliyeTipiSecimi = request.POST.get("ajaxIrsaliyeTipiSecimi")
					# Satış İrsaliyesi Seçildiğinde IrsaliyeNo Tablosundan İrsaliye No Seçilir
					if(ajaxIrsaliyeTipiSecimi):
						try:
							sqlIrsaliyeNo = get_object_or_404(IrsaliyeNo,id="1")
							varIrsaliyeNo = sqlIrsaliyeNo.SatisIrsaliyesiNo
						except:
							varIrsaliyeNo = ""
						context = {"ajaxSqlIrsaliyeNo" : varIrsaliyeNo,}			
						return JsonResponse(context)
					# Seçilen Irsaliye Tipine Göre Stok Fiyatı Seçimi
					ajaxStokKoduStokSecimi     = request.POST.get("ajaxStokKoduStokSecimi")
					ajaxIrsaliyeTipiStokSecimi = request.POST.get("ajaxIrsaliyeTipiStokSecimi")
					if ajaxStokKoduStokSecimi:
						sqlStok = get_object_or_404(Stok, StokKodu=ajaxStokKoduStokSecimi)
						birimFiyati = ""
						if(ajaxIrsaliyeTipiStokSecimi == "1"):
							birimFiyati = sqlStok.SatisFiyati
						if(ajaxIrsaliyeTipiStokSecimi == "2"):
							birimFiyati = sqlStok.AlisFiyati
						context = {
							"birimFiyati"    : str(birimFiyati),
						    "sqlStokKdvOrani": str(sqlStok.KdvOrani),
						    "sqlStokNitelik" : str(sqlStok.StokNitelik),
						}	
						return JsonResponse(context)
					# Satış Irsaliyesi Seçildiğinde Yeteri Miktarda Stok Olup Olmadığı Kontrolu
					ajaxMiktarKontrol   = request.POST.get("ajaxMiktarKontrol")
					ajaxStokKoduKontrol = request.POST.get("ajaxStokKoduKontrol")
					if(ajaxMiktarKontrol):
						sqlStokMiktarKontrol = get_object_or_404(Stok, StokKodu=ajaxStokKoduKontrol)
						if(int(sqlStokMiktarKontrol.StokMiktar) - int(ajaxMiktarKontrol) < 0):
							context = {"ajaxMesaj" : "1"}
						else:
							context = {"ajaxMesaj" : ""}
						return JsonResponse(context)

					ajaxIrsaliyeNo    = request.POST.get("ajaxIrsaliyeNo")
					ajaxIrsaliyeTipi  = request.POST.get("ajaxIrsaliyeTipi")
					ajaxSevkTarihi    = request.POST.get("ajaxSevkTarihi")
					ajaxStokKodu      = request.POST.get("ajaxStokKodu")
					ajaxStokNitelik   = request.POST.get("ajaxNitelik")
					ajaxMiktar        = request.POST.get("ajaxMiktar")
					ajaxBirimFiyat    = request.POST.get("ajaxBirimFiyat")
					ajaxIskontoOrani  = request.POST.get("ajaxIskontoOrani")
					ajaxKdvOrani      = request.POST.get("ajaxKdvOrani")
					if(ajaxStokKodu != None):
						if(ajaxIrsaliyeNo and ajaxIrsaliyeTipi and ajaxSevkTarihi and ajaxStokKodu and ajaxStokNitelik and ajaxMiktar and ajaxBirimFiyat and ajaxKdvOrani):
							sqlIrsaliyeHareketleri = IrsaliyeHareketleri()
							sqlIrsaliyeHareketleri.IrsaliyeNo    = ajaxIrsaliyeNo
							sqlIrsaliyeHareketleri.IrsaliyeTipi  = ajaxIrsaliyeTipi
							sqlIrsaliyeHareketleri.SevkTarihi    = ajaxSevkTarihi
							sqlIrsaliyeHareketleri.StokKodu      = ajaxStokKodu
							sqlIrsaliyeHareketleri.Nitelik       = ajaxStokNitelik
							sqlIrsaliyeHareketleri.Miktar        = ajaxMiktar
							sqlIrsaliyeHareketleri.BirimFiyat    = ajaxBirimFiyat
							sqlIrsaliyeHareketleri.IskontoOrani  = ajaxIskontoOrani
							sqlIrsaliyeHareketleri.KdvOrani      = ajaxKdvOrani
							sqlIrsaliyeHareketleri.save()
							sqlStok = get_object_or_404(Stok, StokKodu=ajaxStokKodu)
							context = {
								"ajaxMesaj"       : "1",
						    	"sqlId"           : sqlIrsaliyeHareketleri.id, 
						        "sqlStokKodu"     : sqlStok.StokAdi,
						        "sqlNitelik"      : sqlIrsaliyeHareketleri.Nitelik,
								"sqlMiktar"       : str(sqlIrsaliyeHareketleri.Miktar),
								"sqlBirimFiyat"   : str(sqlIrsaliyeHareketleri.BirimFiyat),
								"sqlIskontoOrani" : str(sqlIrsaliyeHareketleri.IskontoOrani),
								"sqlKdvOrani"     : str(sqlIrsaliyeHareketleri.KdvOrani),
							} 	
							return JsonResponse(context)
						else:
							context = {"ajaxMesaj" : "Lütfen Formu Boş Bırakmayınız !"}
							return JsonResponse(context)

					ajaxKey              = request.POST.get("ajaxKey")
					ajaxKey2             = request.POST.get("ajaxKey2")
					ajaxCariKodu         = request.POST.get("ajaxCariKodu")
					ajaxIrsaliyeNo   	 = request.POST.get("ajaxIrsaliyeNo")
					ajaxIrsaliyeTipi 	 = request.POST.get("ajaxIrsaliyeTipi")
					ajaxDuzenlenmeTarihi = request.POST.get("ajaxDuzenlenmeTarihi")
					ajaxDuzenlenmeSaati  = request.POST.get("ajaxDuzenlenmeSaati")
					ajaxSevkTarihi	 	 = request.POST.get("ajaxSevkTarihi")
					ajaxSevkSaati	 	 = request.POST.get("ajaxSevkSaati")
					ajaxTeslimEden		 = request.POST.get("ajaxTeslimEden")
					ajaxTeslimAlan	 	 = request.POST.get("ajaxTeslimAlan")
					ajaxTeslimSaati	 	 = request.POST.get("ajaxTeslimSaati")
					ajaxToplamBrutTutar  = request.POST.get("ajaxToplamBrutTutar")
					ajaxToplamKdv        = request.POST.get("ajaxToplamKdv")
					replaceToplamBrutTutar = ajaxToplamBrutTutar.replace(",",".")
					replaceToplamKdv       = ajaxToplamKdv.replace(",",".")
					if (ajaxCariKodu and ajaxIrsaliyeNo and ajaxIrsaliyeTipi and ajaxDuzenlenmeTarihi and ajaxDuzenlenmeSaati and ajaxSevkTarihi and ajaxSevkSaati and ajaxTeslimEden and ajaxTeslimAlan and ajaxTeslimSaati and ajaxToplamBrutTutar and ajaxToplamKdv):
						sqlIrsaliye = Irsaliye()
						sqlIrsaliye.CariKodu         = ajaxCariKodu
						sqlIrsaliye.KullaniciKodu    = request.session["KullaniciKodu"]
						sqlIrsaliye.IrsaliyeNo       = ajaxIrsaliyeNo
						sqlIrsaliye.IrsaliyeTipi     = ajaxIrsaliyeTipi
						sqlIrsaliye.DuzenlenmeTarihi = ajaxDuzenlenmeTarihi
						sqlIrsaliye.DuzenlenmeSaati  = ajaxDuzenlenmeSaati
						sqlIrsaliye.SevkTarihi       = ajaxSevkTarihi
						sqlIrsaliye.SevkSaati        = ajaxSevkSaati
						sqlIrsaliye.TeslimEden       = ajaxTeslimEden
						sqlIrsaliye.TeslimAlan       = ajaxTeslimAlan
						sqlIrsaliye.TeslimSaati      = ajaxTeslimSaati
						sqlIrsaliye.ToplamBrutTutar  = float(replaceToplamBrutTutar)
						sqlIrsaliye.ToplamKdv        = float(replaceToplamKdv)
						sqlIrsaliye.save()
						for i in IrsaliyeHareketleri.objects.filter(IrsaliyeNo=sqlIrsaliye.IrsaliyeNo,IrsaliyeTipi=sqlIrsaliye.IrsaliyeTipi):
							i.IsSaved = True
							i.save()
						try:
							# Irsaliye Kaydı Yapıldıktan Sonra IrsaliyeNo Tablosundan Irsaliye No Arttırımı
							sqlIrsaliyeNoGuncelle = get_object_or_404(IrsaliyeNo,id="1")
							sqlIrsaliyeNoGuncelle.SatisIrsaliyesiNo = int(ajaxIrsaliyeNo) + 1
							sqlIrsaliyeNoGuncelle.save()
						except:
							pass	
						if(ajaxKey and ajaxKey2 != ""):
							try:
								sqlFatura = get_object_or_404(Fatura,FaturaSeri=ajaxKey,FaturaSira=ajaxKey2)
								sqlFatura.IsTransferCache = True
								sqlFatura.save()
								sqlIrsaliyeIsVerified = get_object_or_404(Irsaliye,IrsaliyeTipi=ajaxIrsaliyeTipi,IrsaliyeNo=ajaxIrsaliyeNo)
								sqlIrsaliyeIsVerified.IsVerified = True
								sqlIrsaliyeIsVerified.save()
								for sqlFaturaHareketleri in FaturaHareketleri.objects.filter(FaturaSeri=ajaxKey,FaturaSira=ajaxKey2):
									sqlFaturaHareketleri.IsTransferCache = True
									sqlFaturaHareketleri.save()
									sqlIrsaliyeHareketleri = IrsaliyeHareketleri()
									sqlIrsaliyeHareketleri.IrsaliyeNo    = ajaxIrsaliyeNo
									sqlIrsaliyeHareketleri.IrsaliyeTipi  = ajaxIrsaliyeTipi
									sqlIrsaliyeHareketleri.SevkTarihi    = ajaxSevkTarihi
									sqlIrsaliyeHareketleri.StokKodu      = sqlFaturaHareketleri.StokKodu
									sqlIrsaliyeHareketleri.Nitelik       = sqlFaturaHareketleri.Nitelik
									sqlIrsaliyeHareketleri.Miktar        = sqlFaturaHareketleri.Miktar
									sqlIrsaliyeHareketleri.BirimFiyat    = sqlFaturaHareketleri.BirimFiyat
									sqlIrsaliyeHareketleri.IskontoOrani  = sqlFaturaHareketleri.IskontoOrani
									sqlIrsaliyeHareketleri.KdvOrani      = sqlFaturaHareketleri.KdvOrani
									sqlIrsaliyeHareketleri.IsSaved       = True
									sqlIrsaliyeHareketleri.IsVerified    = True
									sqlIrsaliyeHareketleri.save()
							except:
								print()	
						context = {"ajaxMesaj" : "1",}	
						return JsonResponse(context)
					else:
						context = {"ajaxMesaj" : "Lütfen Formu Boş Bırakmayınız !"}
						return JsonResponse(context)	
				sqlCariKodu        = ""
				sqlFaturaTipi      = ""
				sqlFaturaSeri      = ""
				sqlFaturaSira      = ""
				sqlToplamBrutTutar = ""
				sqlToplamKdv       = ""
				sqlOdenecekTutar   = ""
				sqlIrsaliyeNo      = ""
				try:
					# Irsaliye Modulune Transfer Olan Faturanın Transferini İptal Etme
					faturaIsTransferred = get_object_or_404(Fatura,IsTransferred=True)
					faturaIsTransferred.IsTransferred = False
					faturaIsTransferred.save()
					if(faturaIsTransferred.FaturaTipi == "1"):
						try:
							# Transfer Olan Fatura Satış Faturası İse SatisIrsaliyesiNo Seçimi
							irsaliyeNo = get_object_or_404(IrsaliyeNo,id="1")
							sqlIrsaliyeNo = int(irsaliyeNo.SatisIrsaliyesiNo)
						except:
							sqlIrsaliyeNo = ""
					# Transfer Olan Fatura Bilgilerini Irsaliyeye Aktarımı		
					sqlCariKodu        = faturaIsTransferred.CariKodu
					sqlFaturaTipi      = faturaIsTransferred.FaturaTipi
					sqlFaturaSeri      = faturaIsTransferred.FaturaSeri
					sqlFaturaSira      = faturaIsTransferred.FaturaSira
					sqlToplamBrutTutar = faturaIsTransferred.ToplamBrutTutar
					sqlToplamKdv       = faturaIsTransferred.ToplamKdv
					sqlOdenecekTutar   = float(faturaIsTransferred.ToplamBrutTutar + faturaIsTransferred.ToplamKdv)
					key = "1"			
				except:
					key = "0"
					pass
				try:
					# Transfer Olan Fatura Hareketlerinin Transferinin İptali
					faturaHareketleriIsTransferred = FaturaHareketleri.objects.filter(IsTransferred=True)
					for faturaHareketleri in faturaHareketleriIsTransferred:
						faturaHareketleri.IsTransferred = False
						faturaHareketleri.save()					
				except:
					pass
				try:
					# Kaydedilemeden Çıkış Yapılan İrsaliye Hareketlerinin Silinmesi
					irsaliyeHareketleriSil = IrsaliyeHareketleri.objects.filter(IsSaved=False)
					for i in irsaliyeHareketleriSil:
						i.delete()
				except:
					pass
				sqlCari = Cari.objects.filter(IsDeleted=False)
				sqlStok = Stok.objects.filter(IsDeleted=False)	
				context = {
					"modulYetkisi"                     : modulYetkisi,
					"sqlIrsaliyeNo"					   : sqlIrsaliyeNo,
					"sqlCariKodu"   				   : sqlCariKodu,
					"sqlFaturaTipi"      			   : sqlFaturaTipi,
					"sqlFaturaSeri"					   : sqlFaturaSeri,
					"sqlFaturaSira"					   : sqlFaturaSira,
					"sqlToplamBrutTutar"      		   : sqlToplamBrutTutar,
					"sqlToplamKdv"      		       : sqlToplamKdv,
					"sqlOdenecekTutar"                 : sqlOdenecekTutar,
					"faturaHareketleriIsTransferCache" : faturaHareketleriIsTransferred,
					"suan"                             : suan,
					"sqlCari"                          : sqlCari,
					"sqlStok"                          : sqlStok,
				}
				if(key == "0"):
					return render (request, "irsaliye/olustur.html", context)
				if(key == "1"):
					return render (request, "irsaliye/olusturFatura.html", context)
			else:		
				messages.success(request, "İrsaliye Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def IrsaliyeListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsIrsaliye == True):
			islemlerKontrol = get_object_or_404(IrsaliyeYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsIrsaliyeListele == True):
				if request.is_ajax():
					ajaxDetay 	    = request.POST.get("ajaxDetay")
					if(ajaxDetay):	
						sqlIrsaliye = get_object_or_404(Irsaliye, id=ajaxDetay)
						sqlIrsaliyeHareketleri = IrsaliyeHareketleri.objects.filter(IrsaliyeNo=sqlIrsaliye.IrsaliyeNo,IrsaliyeTipi=sqlIrsaliye.IrsaliyeTipi)
						irsaliyeHareketleriList = []
						for irsaliyeHareketleri in sqlIrsaliyeHareketleri:
							hareketler = [irsaliyeHareketleri.StokKodu,irsaliyeHareketleri.Miktar,\
							irsaliyeHareketleri.Nitelik,irsaliyeHareketleri.BirimFiyat,\
							irsaliyeHareketleri.IskontoOrani,irsaliyeHareketleri.KdvOrani]
							irsaliyeHareketleriList.append(hareketler)

						sqlStok = get_object_or_404(Stok, StokKodu=irsaliyeHareketleri.StokKodu)
						sqlCari = get_object_or_404(Cari, CariKodu=sqlIrsaliye.CariKodu)
						sqlCariIrtibat = get_object_or_404(CariIrtibat, CariKodu=sqlCari.CariKodu)
						if(sqlIrsaliye.IrsaliyeTipi == "1"):
							varIrsaliyeTipi = "Satış İrsaliyesi"
						elif(sqlIrsaliye.IrsaliyeTipi == "2"):
							varIrsaliyeTipi = "Alış İrsaliyesi"
						context = {
							"irsaliyeHareketleriList" : irsaliyeHareketleriList,
							"ajaxIrsaliyeNo"          : sqlIrsaliye.IrsaliyeNo,
							"ajaxIrsaliyeTipi"        : varIrsaliyeTipi,
							"ajaxDuzenlenmeTarihi"    : sqlIrsaliye.DuzenlenmeTarihi,
							"ajaxDuzenlenmeSaati"     : sqlIrsaliye.DuzenlenmeSaati,
							"ajaxSevkTarihi"          : sqlIrsaliye.SevkTarihi,
							"ajaxSevkSaati"           : sqlIrsaliye.SevkSaati,
							"ajaxTeslimEden"          : sqlIrsaliye.TeslimEden,
							"ajaxTeslimAlan"          : sqlIrsaliye.TeslimAlan,
							"ajaxTeslimSaati"         : sqlIrsaliye.TeslimSaati,
							"ajaxCariUnvani"          : sqlCari.CariUnvani,
							"ajaxVergiDairesi"        : sqlCari.VergiDairesi,
							"ajaxVergiNumarasi"       : sqlCari.VergiNumarasi,
							"ajaxAdres"               : sqlCariIrtibat.Adres,
							"ajaxIl"                  : sqlCariIrtibat.Il,
							"ajaxIlce"                : sqlCariIrtibat.Ilce,
							"ajaxTel1"                : sqlCariIrtibat.Tel1,
						}
						return JsonResponse(context)

					ajaxArguman1 = request.POST.get("ajaxArguman1")
					ajaxArguman2 = request.POST.get("ajaxArguman2")	
					if(ajaxArguman1 and ajaxArguman2):
						valueIsTransferred = get_object_or_404(Irsaliye, IrsaliyeNo=ajaxArguman1,IrsaliyeTipi=ajaxArguman2)
						valueIsTransferred.IsTransferred = True
						valueIsTransferred.save()
						for irsaliyeHareketleriIsTransferred in IrsaliyeHareketleri.objects.filter(IrsaliyeNo=ajaxArguman1,IrsaliyeTipi=ajaxArguman2):
							irsaliyeHareketleriIsTransferred.IsTransferred = True
							irsaliyeHareketleriIsTransferred.save()
						context = {"ajaxMesaj": "/fatura/olustur/",}	
						return JsonResponse(context)

					ajaxArguman1Iptal = request.POST.get("ajaxArguman1Iptal")
					ajaxArguman2Iptal = request.POST.get("ajaxArguman2Iptal")
					if(ajaxArguman1Iptal and ajaxArguman2Iptal):
						valueIsCanceled = get_object_or_404(Irsaliye, IrsaliyeNo=ajaxArguman1Iptal,IrsaliyeTipi=ajaxArguman2Iptal)
						valueIsCanceled.IsCanceled = True
						valueIsCanceled.save()
						for irsaliyeHareketleriIsCanceled in IrsaliyeHareketleri.objects.filter(IrsaliyeNo=ajaxArguman1Iptal,IrsaliyeTipi=ajaxArguman2Iptal):
							irsaliyeHareketleriIsCanceled.IsCanceled = True
							irsaliyeHareketleriIsCanceled.save()
						context = {"ajaxMesaj": "İşlem Başarılı",}	
						return JsonResponse(context)

					ajaxArguman1Sil = request.POST.get("ajaxArguman1Sil")
					ajaxArguman2Sil = request.POST.get("ajaxArguman2Sil")
					if(ajaxArguman1Sil and ajaxArguman2Sil):
						valueIsDeleted = get_object_or_404(Irsaliye, IrsaliyeNo=ajaxArguman1Sil,IrsaliyeTipi=ajaxArguman2Sil)
						valueIsDeleted.IsDeleted = True
						valueIsDeleted.save()
						for irsaliyeHareketleriIsDeleted in IrsaliyeHareketleri.objects.filter(IrsaliyeNo=ajaxArguman1Sil,IrsaliyeTipi=ajaxArguman2Sil):
							irsaliyeHareketleriIsDeleted.IsDeleted = True
							irsaliyeHareketleriIsDeleted.save()
						context = {"ajaxMesaj": "İşlem Başarılı",}	
						return JsonResponse(context)

				sqlIrsaliye = Irsaliye.objects.filter(IsCanceled=False)
				sqlIrsaliyeIsCanceled = Irsaliye.objects.filter(IsCanceled=True,IsDeleted=False)
				context = {
					"modulYetkisi" 			: modulYetkisi,
					"islemlerKontrol"       : islemlerKontrol,
					"sqlIrsaliye"           : sqlIrsaliye,
					"sqlIrsaliyeIsCanceled" : sqlIrsaliyeIsCanceled,
				}
				return render (request, "irsaliye/listele.html", context)
			else:		
				messages.success(request, "İrsaliye Listesini Görüntülemeye Yetkiniz Yok !")
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
		if(modulYetkisi.IsIrsaliye == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsIrsaliyeTanimlamalari == True):	
				ajaxSatisIrsaliyesiNo  = request.POST.get("ajaxSatisIrsaliyesiNo")
				try:
					sqlIrsaliyeNo = get_object_or_404(IrsaliyeNo,id="1")
					if request.is_ajax():
						sqlIrsaliyeNo.SatisIrsaliyesiNo  = ajaxSatisIrsaliyesiNo
						sqlIrsaliyeNo.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !"}
						return JsonResponse(context)
				except:
					if request.is_ajax():
						sqlIrsaliyeNoOlustur = IrsaliyeNo()
						sqlIrsaliyeNoOlustur.SatisIrsaliyesiNo  = ajaxSatisIrsaliyesiNo
						sqlIrsaliyeNoOlustur.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !"}
						return JsonResponse(context)
					sqlIrsaliyeNo = ""
				context = {
					"modulYetkisi"  : modulYetkisi,
					"sqlIrsaliyeNo" : sqlIrsaliyeNo,
				}		
				return render (request, "irsaliye/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")		