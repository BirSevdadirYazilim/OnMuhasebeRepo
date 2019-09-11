from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from cari.models import *
from stok.models import *
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404

suan = timezone.now()

def SiparisOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsSiparis == True):
			islemlerKontrol = get_object_or_404(SiparisYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsSiparisOlustur == True):
				if request.is_ajax():
					ajaxSil = request.POST.get("ajaxSil")
					if (ajaxSil):
						sqlFaturaHareketleri = get_object_or_404(SiparisHareketleri, id=ajaxSil)	
						sqlFaturaHareketleri.delete()
						context = {"ajaxMesaj": "Silme İşlemi Başarılı!"}
						return JsonResponse(context)

					siparisTipi = request.POST.get("siparisTipi")
					# Seçilen Siparişe Göre Sipariş Fişi No SiparisFisiNo Tablosundan Çekimi
					if(siparisTipi):
						varSiparisFisiNo = ""
						if(siparisTipi == "2"):
							try:
								sqlSiparisFisiNo = get_object_or_404(SiparisFisiNo,id="1")
								varSiparisFisiNo = sqlSiparisFisiNo.AlınanSiparisFisiNo
							except:
								varSiparisFisiNo = ""
						if(siparisTipi == "1"):
							try:
								sqlSiparisFisiNo = get_object_or_404(SiparisFisiNo,id="1")
								varSiparisFisiNo = sqlSiparisFisiNo.VerilenSiparisFisiNo
							except:
								varSiparisFisiNo = ""
						context = {"siparisFisiNo": varSiparisFisiNo,}									
						return JsonResponse(context)

					ajaxStokKodu    = request.POST.get("ajaxStokKodu")
					ajaxSiparisTipi = request.POST.get("ajaxSiparisTipi")
					if ajaxStokKodu:
						sqlStok = get_object_or_404(Stok, StokKodu=ajaxStokKodu)
						birimFiyati = ""
						if(ajaxSiparisTipi == "2"):
							birimFiyati = sqlStok.SatisFiyati
						if(ajaxSiparisTipi == "1"):
							birimFiyati = sqlStok.AlisFiyati
						context = {
							"sqlStokMiktar"   : str(sqlStok.StokMiktar),
					    	"birimFiyati"     : str(birimFiyati),
					        "sqlStokKdvOrani" : str(sqlStok.KdvOrani),
					        "sqlStokNitelik"  : str(sqlStok.StokNitelik),
						}
						return JsonResponse(context)

					ajaxMiktarKontrol   = request.POST.get("ajaxMiktarKontrol")
					ajaxStokKoduKontrol = request.POST.get("ajaxStokKoduKontrol")
					if(ajaxMiktarKontrol):
						sqlStokMiktarKontrol = get_object_or_404(Stok, StokKodu=ajaxStokKoduKontrol)
						if(int(sqlStokMiktarKontrol.StokMiktar) - int(ajaxMiktarKontrol) < 0):
							context = {"ajaxMesaj" : "1",}
						else:
							context = {"ajaxMesaj" : "",}
						return JsonResponse(context)
						
					ajaxSiparisFisiNoEkle = request.POST.get("ajaxSiparisFisNoEkle")
					ajaxSiparisTipiEkle   = request.POST.get("ajaxSiparisTipiEkle")
					ajaxSiparisTarihiEkle = request.POST.get("ajaxSiparisTarihiEkle")
					ajaxStokKoduEkle      = request.POST.get("ajaxStokKoduEkle")
					ajaxStokNitelikEkle   = request.POST.get("ajaxNitelikEkle")
					ajaxMiktarEkle        = request.POST.get("ajaxMiktarEkle")
					ajaxBirimFiyatEkle    = request.POST.get("ajaxBirimFiyatEkle")
					ajaxIskontoOraniEkle  = request.POST.get("ajaxIskontoOraniEkle")
					ajaxKdvOraniEkle      = request.POST.get("ajaxKdvOraniEkle")
					if ajaxStokKoduEkle:
						if(ajaxSiparisFisiNoEkle and ajaxSiparisTipiEkle and ajaxSiparisTarihiEkle and ajaxStokKoduEkle and ajaxStokNitelikEkle and ajaxMiktarEkle and ajaxBirimFiyatEkle and ajaxKdvOraniEkle):
							sqlSiparisHareketleri = SiparisHareketleri()
							sqlSiparisHareketleri.SiparisFisiNo = ajaxSiparisFisiNoEkle
							sqlSiparisHareketleri.SiparisTipi   = ajaxSiparisTipiEkle
							sqlSiparisHareketleri.SiparisTarihi = ajaxSiparisTarihiEkle
							sqlSiparisHareketleri.StokKodu      = ajaxStokKoduEkle
							sqlSiparisHareketleri.Nitelik       = ajaxStokNitelikEkle
							sqlSiparisHareketleri.Miktar        = ajaxMiktarEkle
							sqlSiparisHareketleri.BirimFiyat    = ajaxBirimFiyatEkle
							sqlSiparisHareketleri.IskontoOrani  = ajaxIskontoOraniEkle
							sqlSiparisHareketleri.KdvOrani      = ajaxKdvOraniEkle
							sqlSiparisHareketleri.save()
		
							sqlStok = get_object_or_404(Stok, StokKodu=ajaxStokKoduEkle)
							context = {
								"ajaxMesaj"       : "1",
								"sqlId"           : sqlSiparisHareketleri.id, 
						        "sqlStokKodu"     : sqlStok.StokAdi,
						        "sqlNitelik"      : sqlSiparisHareketleri.Nitelik,
								"sqlMiktar"       : str(sqlSiparisHareketleri.Miktar),
								"sqlBirimFiyat"   : str(sqlSiparisHareketleri.BirimFiyat),
								"sqlIskontoOrani" : str(sqlSiparisHareketleri.IskontoOrani),
								"sqlKdvOrani"     : str(sqlSiparisHareketleri.KdvOrani),
							}
						else:
							context = {"ajaxMesaj" : "Lütfen Formu Boş Bırakmayınız !"}
						return JsonResponse(context)

					ajaxCariKodu        = request.POST.get("ajaxCariKodu")
					ajaxSiparisFisiNo   = request.POST.get("ajaxSiparisFisiNo")
					ajaxSiparisTipi     = request.POST.get("ajaxSiparisTipi")
					ajaxSiparisTarihi   = request.POST.get("ajaxSiparisTarihi")
					ajaxToplamBrutTutar = request.POST.get("ajaxToplamBrutTutar")
					ajaxToplamKdv       = request.POST.get("ajaxToplamKdv")
					if(ajaxCariKodu and ajaxSiparisFisiNo and ajaxSiparisTipi and ajaxToplamBrutTutar and ajaxToplamKdv):
						sqlSiparis = Siparis()
						sqlSiparis.CariKodu        = ajaxCariKodu
						sqlSiparis.KullaniciKodu   = request.session["KullaniciKodu"]
						sqlSiparis.SiparisFisiNo   = ajaxSiparisFisiNo
						sqlSiparis.SiparisTipi     = ajaxSiparisTipi
						sqlSiparis.SiparisTarihi   = ajaxSiparisTarihi
						sqlSiparis.ToplamBrutTutar = float(ajaxToplamBrutTutar)
						sqlSiparis.ToplamKdv       = float(ajaxToplamKdv)
						sqlSiparis.save()
						for sqlSiparisHareketleriIsVerified in SiparisHareketleri.objects.filter(SiparisFisiNo=sqlSiparis.SiparisFisiNo,SiparisTipi=sqlSiparis.SiparisTipi):
							sqlSiparisHareketleriIsVerified.IsSaved = True
							sqlSiparisHareketleriIsVerified.save()
						try:
							sqlSiparisFisiNo = get_object_or_404(SiparisFisiNo,id="1")
							if(ajaxSiparisTipi == "2"):
								sqlSiparisFisiNo.AlınanSiparisFisiNo = int(ajaxSiparisFisiNo) + 1
								sqlSiparisFisiNo.save()
							if(ajaxSiparisTipi == "1"):
								sqlSiparisFisiNo.VerilenSiparisFisiNo = int(ajaxSiparisFisiNo) + 1	
								sqlSiparisFisiNo.save()
						except:
							pass		
						context = {"ajaxMesaj": "1",}
					else:
						context = {"ajaxMesaj": "Lütfen Formu Boş Bırakmayınız !",}
					return JsonResponse(context)	
				sqlCari = Cari.objects.filter(IsDeleted=False)
				sqlStok = Stok.objects.filter(IsDeleted=False)
				try:
					for siparisHareketleriSil in SiparisHareketleri.objects.filter(IsSaved=False):
						siparisHareketleriSil.delete()
				except:
					pass	
				context = {
					"modulYetkisi" : modulYetkisi,
					"suan"         : suan,
					"sqlCari"      : sqlCari,
					"sqlStok"      : sqlStok,
				}
				return render (request, "siparis/olustur.html", context)
			else:		
				messages.success(request, "Sipariş Oluşturma Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def SiparisListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsSiparis == True):
			islemlerKontrol = get_object_or_404(SiparisYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsSiparisListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlSiparisDetay = get_object_or_404(Siparis, id=ajaxDetay)
						sqlSiparisHarDetay = SiparisHareketleri.objects.filter(SiparisFisiNo=sqlSiparisDetay.SiparisFisiNo,SiparisTipi=sqlSiparisDetay.SiparisTipi)
						siparisHareketleriList = []	
						for siparisHarDetay in sqlSiparisHarDetay:
							hareketler = [siparisHarDetay.StokKodu,siparisHarDetay.Miktar,siparisHarDetay.Nitelik,\
							siparisHarDetay.BirimFiyat,siparisHarDetay.IskontoOrani,siparisHarDetay.KdvOrani]
							siparisHareketleriList.append(hareketler)
						sqlStokDetay = get_object_or_404(Stok, StokKodu=siparisHarDetay.StokKodu)
						sqlCariDetay = get_object_or_404(Cari, CariKodu=sqlSiparisDetay.CariKodu)
						sqlCariIrtibatDetay = get_object_or_404(CariIrtibat, CariKodu=sqlCariDetay.CariKodu)	
						if(sqlSiparisDetay.SiparisTipi == "1"):
							varSiparisTipi = "Verilen Sipariş"
						elif(sqlSiparisDetay.SiparisTipi == "2"):
							varSiparisTipi = "Alınan Sipariş"	
						context = {
							"siparisHareketleriList" : siparisHareketleriList,
							"ajaxSiparisFisiNo"      : sqlSiparisDetay.SiparisFisiNo,
							"ajaxSiparisTipi"        : varSiparisTipi,
							"ajaxSiparisTarihi"      : sqlSiparisDetay.SiparisTarihi,
							"ajaxToplamBrutTutar"    : sqlSiparisDetay.ToplamBrutTutar,
							"ajaxToplamKdv"          : sqlSiparisDetay.ToplamKdv,
							"ajaxCariUnvani"         : sqlCariDetay.CariUnvani,
							"ajaxVergiDairesi"       : sqlCariDetay.VergiDairesi,
							"ajaxVergiNumarasi"      : sqlCariDetay.VergiNumarasi,
							"ajaxAdres"              : sqlCariIrtibatDetay.Adres,
							"ajaxIl"                 : sqlCariIrtibatDetay.Il,
							"ajaxIlce"               : sqlCariIrtibatDetay.Ilce,
							"ajaxTel1"               : sqlCariIrtibatDetay.Tel1,
						}
						return JsonResponse(context)

					ajaxSiparisFisiNo = request.POST.get("ajaxSiparisFisiNo")
					ajaxSiparisTipi   = request.POST.get("ajaxSiparisTipi")	
					if(ajaxSiparisFisiNo and ajaxSiparisTipi):
						valueIsTransferred = get_object_or_404(Siparis, SiparisFisiNo=ajaxSiparisFisiNo,SiparisTipi=ajaxSiparisTipi)
						valueIsTransferred.IsTransferred = True
						valueIsTransferred.save()
						for siparisHareketleriIsTransferred in SiparisHareketleri.objects.filter(SiparisFisiNo=ajaxSiparisFisiNo,SiparisTipi=ajaxSiparisTipi):
							siparisHareketleriIsTransferred.IsTransferred = True
							siparisHareketleriIsTransferred.save()
						context = {"ajaxMesaj": "/fatura/olustur/",}		
						return JsonResponse(context)	

					ajaxSipFisNoIptal = request.POST.get("ajaxSipFisNoIptal")
					ajaxSipTipIptal   = request.POST.get("ajaxSipTipIptal")
					if(ajaxSipFisNoIptal and ajaxSipTipIptal):
						valueIsCanceled = get_object_or_404(Siparis, SiparisFisiNo=ajaxSipFisNoIptal,SiparisTipi=ajaxSipTipIptal)
						valueIsCanceled.IsCanceled = True
						valueIsCanceled.save()
						for siparisHareketleriIsCanceled in SiparisHareketleri.objects.filter(SiparisFisiNo=ajaxSipFisNoIptal,SiparisTipi=ajaxSipTipIptal):
							siparisHareketleriIsCanceled.IsCanceled = True
							siparisHareketleriIsCanceled.save()
						context = {"ajax": "Başarılı",}		
						return JsonResponse(context)

					argument1Sil = request.POST.get("argument1Sil")
					argument2Sil = request.POST.get("argument2Sil")
					if(argument1Sil and argument2Sil):
						valueIsDeleled = get_object_or_404(Siparis, SiparisFisiNo=argument1Sil,SiparisTipi=argument2Sil)
						valueIsDeleled.IsDeleted = True
						valueIsDeleled.save()
						for i in SiparisHareketleri.objects.filter(SiparisFisiNo=argument1Sil,SiparisTipi=argument2Sil):
							i.IsDeleted = True
							i.save()
						context = {"ajax": "Başarılı",}		
						return JsonResponse(context)	
			
				sqlSiparis = Siparis.objects.filter(IsCanceled=False)
				sqlSiparisIsCanceled = Siparis.objects.filter(IsCanceled=True,IsDeleted=False)
				context = {
					"modulYetkisi" 		   : modulYetkisi,
					"islemlerKontrol"      : islemlerKontrol,
					"sqlSiparis"           : sqlSiparis,
					"sqlSiparisIsCanceled" : sqlSiparisIsCanceled,
				}
				return render (request, "siparis/listele.html", context)
			else:		
				messages.success(request, "Sipariş Listesini Görüntüleme Yetkiniz Yok !")
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
		if(modulYetkisi.IsSiparis == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsSiparisTanimlamalari == True):
				ajaxAlınanSiparisFisiNo  = request.POST.get("ajaxAlınanSiparisFisiNo")
				ajaxVerilenSiparisFisiNo = request.POST.get("ajaxVerilenSiparisFisiNo")
				try:
					sqlSiparisFisiNo = get_object_or_404(SiparisFisiNo,id="1")
					if request.is_ajax():
						sqlSiparisFisiNo.AlınanSiparisFisiNo  = ajaxAlınanSiparisFisiNo
						sqlSiparisFisiNo.VerilenSiparisFisiNo = ajaxVerilenSiparisFisiNo
						sqlSiparisFisiNo.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)
				except:
					if request.is_ajax():
						sqlSiparisFisiNoOlustur = SiparisFisiNo()
						sqlSiparisFisiNoOlustur.AlınanSiparisFisiNo  = ajaxAlınanSiparisFisiNo
						sqlSiparisFisiNoOlustur.VerilenSiparisFisiNo = ajaxVerilenSiparisFisiNo
						sqlSiparisFisiNoOlustur.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)
					sqlSiparisFisiNo = ""
				context = {
					"modulYetkisi" 	   : modulYetkisi,
					"sqlSiparisFisiNo" : sqlSiparisFisiNo,
				}		
				return render (request, "siparis/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")				