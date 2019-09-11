from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from fatura.models import *
from siparis.models import *
from irsaliye.models import *
from kasa.models import *
from banka.models import *
from ceksenet.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
def CariOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCari == True):
			islemlerKontrol = get_object_or_404(CariYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsCariOlustur == True):
				if request.is_ajax():	     
					ajaxCariKodu   	  = request.POST.get("ajaxCariKodu")
					ajaxCariUnvani    = request.POST.get("ajaxCariUnvani")
					ajaxVergiDairesi  = request.POST.get("ajaxVergiDairesi")
					ajaxVergiNumarasi = request.POST.get("ajaxVergiNumarasi")
					ajaxIl 		      = request.POST.get("ajaxIl")
					ajaxIlce 		  = request.POST.get("ajaxIlce")
					ajaxAdres 		  = request.POST.get("ajaxAdres")
					ajaxPostaKodu 	  = request.POST.get("ajaxPostaKodu")
					ajaxKEP           = request.POST.get("ajaxKEP")
					ajaxTel1 		  = request.POST.get("ajaxTel1")
					ajaxTel2		  = request.POST.get("ajaxTel2")
					ajaxEmail 		  = request.POST.get("ajaxEmail")
					ajaxWebSitesi 	  = request.POST.get("ajaxWebSitesi")
					ajaxLokasyonKodu  = request.POST.get("ajaxLokasyonKodu")
					ajaxLokasyonDetay = request.POST.get("ajaxLokasyonDetay")
					try:
						cariKoduKontrol = get_object_or_404(Cari,CariKodu=ajaxCariKodu)
						context = {"ajaxMesaj" : "Bu Cari Kodu Kullanılıyor !"}
						return JsonResponse(context)
					except:
						pass
					try:
						cariUnvaniKontrol = get_object_or_404(Cari,CariUnvani=ajaxCariUnvani)
						context = {"ajaxMesaj" : "Bu Cari Unvanı Kullanılıyor !"}
						return JsonResponse(context)
					except:
						pass	
					if(ajaxCariKodu and ajaxCariUnvani and ajaxVergiDairesi and ajaxVergiNumarasi and ajaxIl and ajaxIlce and ajaxAdres and ajaxPostaKodu and ajaxTel1):
						sqlCari = Cari()
						sqlCari.CariKodu 	  = ajaxCariKodu
						sqlCari.CariUnvani    = ajaxCariUnvani
						sqlCari.VergiDairesi  = ajaxVergiDairesi
						sqlCari.VergiNumarasi = ajaxVergiNumarasi
						sqlCari.save()

						sqlCariIrtibat = CariIrtibat()
						sqlCariIrtibat.CariKodu     = ajaxCariKodu
						sqlCariIrtibat.Il           = ajaxIl
						sqlCariIrtibat.Ilce         = ajaxIlce
						sqlCariIrtibat.Adres        = ajaxAdres
						sqlCariIrtibat.KEP          = ajaxKEP
						sqlCariIrtibat.PostaKodu    = ajaxPostaKodu
						sqlCariIrtibat.Tel1         = ajaxTel1
						sqlCariIrtibat.Tel2         = ajaxTel2
						sqlCariIrtibat.Email        = ajaxEmail
						sqlCariIrtibat.WebSitesi    = ajaxWebSitesi
						sqlCariIrtibat.save()

						sqlCariLokasyon = CariLokasyon()
						sqlCariLokasyon.CariKodu      = ajaxCariKodu
						sqlCariLokasyon.LokasyonKodu  = ajaxLokasyonKodu
						sqlCariLokasyon.LokasyonDetay = ajaxLokasyonDetay
						sqlCariLokasyon.save()

						context = {"ajaxMesaj" : "1",}
						return JsonResponse(context)
					else:
						context = {"ajaxMesaj" : "Lütfen Formu Boş Bırakmayınız !",}
						return JsonResponse(context)		
				context = {"modulYetkisi" : modulYetkisi,}
				return render (request, "cari/olustur.html", context)
			else:		
				messages.success(request, "Cari Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")		

def CariListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCari == True):
			islemlerKontrol = get_object_or_404(CariYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsCariListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlCari    = get_object_or_404(Cari, id=ajaxDetay)
						sqlCariIrtibat  = get_object_or_404(CariIrtibat, CariKodu=sqlCari.CariKodu)
						sqlCariLokasyon = get_object_or_404(CariLokasyon, CariKodu=sqlCari.CariKodu)
						context = {
							"ajaxCariKodu"      : sqlCari.CariKodu,
							"ajaxCariUnvani"    : sqlCari.CariUnvani,
							"ajaxVergiDairesi"  : sqlCari.VergiDairesi,
							"ajaxVergiNumarasi" : sqlCari.VergiNumarasi,
							"ajaxIl"            : sqlCariIrtibat.Il,
							"ajaxIlce"          : sqlCariIrtibat.Ilce,
							"ajaxAdres"         : sqlCariIrtibat.Adres,
							"ajaxPostaKodu"     : sqlCariIrtibat.PostaKodu,
							"ajaxKEP"           : sqlCariIrtibat.KEP,
							"ajaxTel1"          : sqlCariIrtibat.Tel1,
							"ajaxTel2"          : sqlCariIrtibat.Tel2,
							"ajaxEmail"         : sqlCariIrtibat.Email,
							"ajaxWebSitesi"     : sqlCariIrtibat.WebSitesi,
							"ajaxLokasyonKodu"  : sqlCariLokasyon.LokasyonKodu,
							"ajaxLokasyonDetay" : sqlCariLokasyon.LokasyonDetay,
						}
						return JsonResponse(context)
						
					ajaxGuncelle = request.POST.get("ajaxGuncelle")
					if(ajaxGuncelle):
						sqlCariGuncelle         = get_object_or_404(Cari, id=ajaxGuncelle)
						sqlCariIrtibatGuncelle  = get_object_or_404(CariIrtibat, CariKodu=sqlCariGuncelle.CariKodu)
						sqlCariLokasyonGuncelle = get_object_or_404(CariLokasyon, CariKodu=sqlCariGuncelle.CariKodu)
						context = {
							"ajaxIdGuncelle"            : sqlCariGuncelle.id,
							"ajaxCariKoduGuncelle"      : sqlCariGuncelle.CariKodu,
							"ajaxCariUnvaniGuncelle"    : sqlCariGuncelle.CariUnvani,
							"ajaxVergiDairesiGuncelle"  : sqlCariGuncelle.VergiDairesi,
							"ajaxVergiNumarasiGuncelle" : sqlCariGuncelle.VergiNumarasi,
							"ajaxIdGuncelle2"           : sqlCariIrtibatGuncelle.id,
							"ajaxIlGuncelle"            : sqlCariIrtibatGuncelle.Il,
							"ajaxIlceGuncelle"          : sqlCariIrtibatGuncelle.Ilce,
							"ajaxAdresGuncelle"         : sqlCariIrtibatGuncelle.Adres,
							"ajaxPostaKoduGuncelle"     : sqlCariIrtibatGuncelle.PostaKodu,
							"ajaxKEPGuncelle"           : sqlCariIrtibatGuncelle.KEP,
							"ajaxTel1Guncelle"          : sqlCariIrtibatGuncelle.Tel1,
							"ajaxTel2Guncelle"          : sqlCariIrtibatGuncelle.Tel2,
							"ajaxEmailGuncelle"         : sqlCariIrtibatGuncelle.Email,
							"ajaxWebSitesiGuncelle"     : sqlCariIrtibatGuncelle.WebSitesi,
							"ajaxIdGuncelle3"  			: sqlCariLokasyonGuncelle.id,
							"ajaxLokasyonKoduGuncelle"  : sqlCariLokasyonGuncelle.LokasyonKodu,
							"ajaxLokasyonDetayGuncelle" : sqlCariLokasyonGuncelle.LokasyonDetay,
						}
						return JsonResponse(context)

					ajaxIdKaydet            = request.POST.get("ajaxIdKaydet")
					ajaxIdKaydet2           = request.POST.get("ajaxIdKaydet2")
					ajaxIdKaydet3           = request.POST.get("ajaxIdKaydet3")	
					ajaxCariKoduKaydet      = request.POST.get("ajaxCariKoduKaydet")
					ajaxCariUnvaniKaydet    = request.POST.get("ajaxCariUnvaniKaydet")
					ajaxVergiDairesiKaydet  = request.POST.get("ajaxVergiDairesiKaydet")
					ajaxVergiNumarasiKaydet = request.POST.get("ajaxVergiNumarasiKaydet")
					ajaxKEPKaydet           = request.POST.get("ajaxKEPKaydet")
					ajaxIlKaydet            = request.POST.get("ajaxIlKaydet")
					ajaxIlceKaydet          = request.POST.get("ajaxIlceKaydet")
					ajaxAdresKaydet         = request.POST.get("ajaxAdresKaydet")
					ajaxPostaKoduKaydet     = request.POST.get("ajaxPostaKoduKaydet")
					ajaxTel1Kaydet          = request.POST.get("ajaxTel1Kaydet")
					ajaxTel2Kaydet          = request.POST.get("ajaxTel2Kaydet")
					ajaxEmailKaydet         = request.POST.get("ajaxEmailKaydet")
					ajaxWebSitesiKaydet     = request.POST.get("ajaxWebSitesiKaydet")
					ajaxLokasyonKoduKaydet  = request.POST.get("ajaxLokasyonKoduKaydet")
					ajaxLokasyonDetayKaydet = request.POST.get("ajaxLokasyonDetayKaydet")
					if(ajaxIdKaydet):
						sqlCariKaydet         = get_object_or_404(Cari, id=ajaxIdKaydet)
						sqlCariKaydet.CariKodu      = ajaxCariKoduKaydet
						sqlCariKaydet.CariUnvani    = ajaxCariUnvaniKaydet
						sqlCariKaydet.VergiDairesi  = ajaxVergiDairesiKaydet
						sqlCariKaydet.VergiNumarasi = ajaxVergiNumarasiKaydet
						sqlCariKaydet.save()

						sqlCariIrtibatKaydet  = get_object_or_404(CariIrtibat, id=ajaxIdKaydet2)
						sqlCariIrtibatKaydet.CariKodu     = ajaxCariKoduKaydet
						sqlCariIrtibatKaydet.Il           = ajaxIlKaydet
						sqlCariIrtibatKaydet.Ilce         = ajaxIlceKaydet
						sqlCariIrtibatKaydet.Adres        = ajaxAdresKaydet
						sqlCariIrtibatKaydet.PostaKodu    = ajaxPostaKoduKaydet
						sqlCariIrtibatKaydet.KEP          = ajaxKEPKaydet
						sqlCariIrtibatKaydet.Tel1         = ajaxTel1Kaydet
						sqlCariIrtibatKaydet.Tel2         = ajaxTel2Kaydet
						sqlCariIrtibatKaydet.Email        = ajaxEmailKaydet
						sqlCariIrtibatKaydet.WebSitesi    = ajaxWebSitesiKaydet
						sqlCariIrtibatKaydet.save()

						sqlCariLokasyonKaydet = get_object_or_404(CariLokasyon, id=ajaxIdKaydet3)
						sqlCariLokasyonKaydet.CariKodu      = ajaxCariKoduKaydet
						sqlCariLokasyonKaydet.LokasyonKodu  = ajaxLokasyonKoduKaydet
						sqlCariLokasyonKaydet.LokasyonDetay = ajaxLokasyonDetayKaydet
						sqlCariLokasyonKaydet.save()
						context = {"ajaxMesaj":"Başarıyla Güncellendi !",}
						return JsonResponse(context)
					
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						sqlCariSil = get_object_or_404(Cari, id=ajaxSil)
						sqlCariSil.IsDeleted = True
						sqlCariSil.save()
						sqlCariIrtibatSil  = get_object_or_404(CariIrtibat,CariKodu=sqlCariSil.CariKodu)
						sqlCariIrtibatSil.IsDeleted = True 
						sqlCariIrtibatSil.save()
						sqlCariLokasyonSil = get_object_or_404(CariLokasyon,CariKodu=sqlCariSil.CariKodu)
						sqlCariLokasyonSil.IsDeleted = True
						sqlCariLokasyonSil.save()
						context = {"ajaxMesaj":"Silme İşlemi Başarılı !",}
						return JsonResponse(context)
				liste = []
				for cari in Cari.objects.filter(IsDeleted=False):
					borc               = 0
					alacak             = 0
					tutarSatisFaturası = 0
					tutarAlisFaturası  = 0
					kalanBakiye        = 0
					try:
						borcBanka = 0
						alacakBanka = 0
						for banka in BankaHareketleri.objects.filter(CariKodu=cari.CariKodu,IsCanceled=False):
							if(banka.BankaBorc != None):
								borcBanka   = banka.BankaBorc + borcBanka
							if(banka.BankaAlacak != None):
								alacakBanka = banka.BankaAlacak + alacakBanka
						borc = borc + borcBanka
						alacak = alacak + alacakBanka	
					except:
						pass
					try:
						borcKasa = 0
						alacakKasa = 0
						for kasa in KasaHareketleri.objects.filter(CariKodu=cari.CariKodu,IsCanceled=False):
							if(kasa.KasaBorc != None):
								borcKasa = kasa.KasaBorc + borcKasa
							if(kasa.KasaAlacak != None):
								alacakKasa = kasa.KasaAlacak + alacakKasa
						borc = borc + borcKasa
						alacak = alacak + alacakKasa	
					except:
						pass
					try:
						borcCek = 0
						alacakCek = 0
						for cek in Cek.objects.filter(CariKodu=cari.CariKodu,IsCanceled=False):
							if(cek.Tipi == "1"):
								borcCek = borcCek + cek.Tutar
							else:
								alacakCek = alacakCek + cek.Tutar
						borc   = borc + borcCek
						alacak = alacak + alacakCek	
					except:
						pass
					try:
						borcSenet = 0
						alacakSenet = 0
						for senet in Senet.objects.filter(CariKodu=cari.CariKodu,IsCanceled=False):
							if(senet.Tipi == "1"):
								borcSenet = borcSenet + senet.Tutar
							else:
								alacakSenet = alacakSenet + senet.Tutar
						borc   = borc + borcSenet
						alacak = alacak + alacakSenet	
					except:
						pass	
					try:
						tutarSatisFaturası = 0
						tutarAlisFaturası = 0
						for fatura in Fatura.objects.filter(CariKodu=cari.CariKodu,IsCanceled=False):
							if(fatura.FaturaTipi == "1"):
								tutarSatisFaturası = (fatura.ToplamBrutTutar + fatura.ToplamKdv) + tutarSatisFaturası
							else:
								tutarAlisFaturası = (fatura.ToplamBrutTutar + fatura.ToplamKdv) + tutarAlisFaturası
						borc   = borc + tutarAlisFaturası
						alacak = alacak + tutarSatisFaturası
					except:
						pass
					demet = {"id":cari.id,"CariKodu":cari.CariKodu,"CariUnvani":cari.CariUnvani,"borc":borc,"alacak":alacak,"kalanBakiye": borc - alacak}
					liste.append(demet)
				context = {
					"modulYetkisi"    : modulYetkisi,
					"islemlerKontrol" : islemlerKontrol,
					"liste" 	      : liste,
				}
				return render (request, "cari/listele.html", context)
			else:		
				messages.success(request, "Cari Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")
			
def CariHareketleri(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCari == True):
			islemlerKontrol = get_object_or_404(CariHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsCariHareketleriListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					ajaxDetayHesap = request.POST.get("ajaxDetayHesap")
					if(ajaxDetay != None or ajaxDetay != ""):
						kolonAdiListesi = ""
						belgeBilgileri  = ""
						if(ajaxDetayHesap == "Fatura"):
							try:
								sqlFaturaDetay = get_object_or_404(Fatura,id=ajaxDetay)
								kolonAdiListesi = ["Cari Kodu","Fatura Seri",\
								"Fatura Sıra","Fatura Tipi","İşlem Tarihi","Toplam Brüt Tutar","Toplam Kdv"]
								if(sqlFaturaDetay.FaturaTipi == "1"):
									faturaTipi = "Satış Faturası"
								else:
									faturaTipi = "Alış Faturası"	
								belgeBilgileri = [sqlFaturaDetay.CariKodu,sqlFaturaDetay.FaturaSeri,\
							    sqlFaturaDetay.FaturaSira, faturaTipi,sqlFaturaDetay.IslemTarihi,\
							    sqlFaturaDetay.ToplamBrutTutar, sqlFaturaDetay.ToplamKdv]
							except:
								pass
						if(ajaxDetayHesap == "Irsaliye"):		
							try:
								sqlIrsaliyeDetay = get_object_or_404(Irsaliye,id=ajaxDetay)
								kolonAdiListesi = ["İrsaliye No","İrsaliye Tipi","Düzenleme Tarihi",\
								"Düzenleme Saati","Sevk Tarihi","Sevk Saati","Teslim Eden","Teslim Alan",\
								"Teslim Saati","Cari Kodu"]
								if(sqlIrsaliyeDetay.IrsaliyeTipi == "1"):
									irsaliyeTipi = "Satış İrsaliyesi"
								else:
									irsaliyeTipi = "Alış İrsaliyesi"	
								belgeBilgileri = [sqlIrsaliyeDetay.IrsaliyeNo,irsaliyeTipi,\
								sqlIrsaliyeDetay.DuzenlenmeTarihi,sqlIrsaliyeDetay.DuzenlenmeSaati,\
								sqlIrsaliyeDetay.SevkTarihi,sqlIrsaliyeDetay.SevkSaati,\
								sqlIrsaliyeDetay.TeslimEden,sqlIrsaliyeDetay.TeslimAlan,\
								sqlIrsaliyeDetay.TeslimSaati,sqlIrsaliyeDetay.CariKodu]
								
							except:
								pass
						if(ajaxDetayHesap == "Siparis"):
							try:
								sqlSiparisDetay = get_object_or_404(Siparis,id=ajaxDetay)
								kolonAdiListesi = ["Cari Kodu","Sipariş Fişi No","Sipariş Tipi","Sipariş Tarihi",\
								"Toplam Brüt Tutar","Toplam Kdv"]
								if(sqlSiparisDetay.SiparisTipi == "1"):
									siparisTipi = "Verilen Sipariş"
								else:
									siparisTipi = "Alınan Sipariş"
								belgeBilgileri = [sqlSiparisDetay.CariKodu,sqlSiparisDetay.SiparisFisiNo,\
								siparisTipi,sqlSiparisDetay.SiparisTarihi,\
								sqlSiparisDetay.ToplamBrutTutar,sqlSiparisDetay.ToplamKdv,]
							except:
								pass
						if(ajaxDetayHesap == "Kasa"):
							try:
								sqlKasaDetay = get_object_or_404(KasaHareketleri,id=ajaxDetay)
								if(sqlKasaDetay.KasaBorc == None):
									kasaBorc = ""
								else:
									kasaBorc = sqlKasaDetay.KasaBorc	
								if(sqlKasaDetay.KasaAlacak == None):
									kasaAlacak = ""
								else:
									kasaAlacak = sqlKasaDetay.KasaAlacak	
								if(sqlKasaDetay.Makbuz == "1"):
									makbuz = "Tahsilat Makbuzu"
								if(sqlKasaDetay.Makbuz == "2"):
									makbuz = "Tediye Makbuzu"		
								kolonAdiListesi = ["Kasa Kodu","Kasa Borc","Kasa Alacak",\
								"Makbuz","Makbuz No","Makbuz Tarihi","Açıklama","Cari Kodu"]
								belgeBilgileri = [sqlKasaDetay.KasaKodu,kasaBorc,kasaAlacak,makbuz,\
								sqlKasaDetay.MakbuzNo,sqlKasaDetay.MakbuzTarihi,sqlKasaDetay.Aciklama,sqlKasaDetay.CariKodu]
							except:
								pass

						if(ajaxDetayHesap == "Banka"):
							try:	
								sqlBankaDetay = get_object_or_404(BankaHareketleri,id=ajaxDetay)
								sqlBankaDetay1 = get_object_or_404(Banka,BankaKodu=sqlBankaDetay.BankaKodu)      
								kolonAdiListesi = ["Banka Kodu","Banka Borc","Banka Alacak",\
								"Dekont","Dekont No","Dekont Tarihi","Açıklama","Cari Kodu"]
								if(sqlBankaDetay.BankaBorc == None):
									bankaBorc = ""
								else:
									bankaBorc = sqlBankaDetay.BankaBorc
								if(sqlBankaDetay.BankaAlacak == None):
									bankaAlacak = ""
								else:
									bankaAlacak = sqlBankaDetay.BankaAlacak
								if(sqlBankaDetay.Dekont == "1"):
									dekont = "Tahsilat Dekontu"		
								else:
									dekont = "Tediye Dekontu"	
								belgeBilgileri = [sqlBankaDetay.BankaKodu,bankaBorc,\
								bankaAlacak,dekont,sqlBankaDetay.DekontNo,\
								sqlBankaDetay.DekontTarihi,sqlBankaDetay.Aciklama,sqlBankaDetay.CariKodu]
							except:
								pass	
						if(ajaxDetayHesap == "Cek"):
							try:
								sqlCekDetay = get_object_or_404(Cek,id=ajaxDetay)
								kolonAdiListesi = ["Bordro No","Bordro Tarihi","Çek No","Tipi",\
								"Durum","Vade","Tutar","Döviz","Cari Kodu","Banka Adı","Şube Kodu","Hesap No","Ödeme Yeri"]
								if(sqlCekDetay.Tipi == "1"):
									tipi = "Alınan Çek"
								if(sqlCekDetay.Tipi == "2"):
									tipi = "Verilen Çek"			
								belgeBilgileri = [sqlCekDetay.BordroNo,sqlCekDetay.BordroTarihi,sqlCekDetay.CekNo,\
								tipi,sqlCekDetay.Durum,sqlCekDetay.Vade,sqlCekDetay.Tutar,sqlCekDetay.Doviz,\
								sqlCekDetay.CariKodu,sqlCekDetay.BankaAdi,sqlCekDetay.SubeKodu,sqlCekDetay.HesapNo,\
								sqlCekDetay.OdemeYeri]
							except:
								print("pass")
								pass

						if(ajaxDetayHesap == "Senet"):
							try:
								sqlSenetDetay = get_object_or_404(Senet,id=ajaxDetay)
								kolonAdiListesi = ["Bordro No","Bordro Tarihi","Senet No","Tipi",\
								"Durum","Vade","Tutar","Döviz","Cari Kodu","Ödeme Yeri"]
								if(sqlSenetDetay.Tipi == "1"):
									tipi = "Alınan Senet"
								if(sqlSenetDetay.Tipi == "2"):
									tipi = "Verilen Senet"		
								belgeBilgileri = [sqlSenetDetay.BordroNo,sqlSenetDetay.BordroTarihi,sqlSenetDetay.SenetNo,\
								tipi,sqlSenetDetay.Durum,sqlSenetDetay.Vade,sqlSenetDetay.Tutar,sqlSenetDetay.Doviz,\
								sqlSenetDetay.CariKodu,sqlSenetDetay.OdemeYeri]
							except:
								pass
						context = {
							"kolonAdiListesi" : kolonAdiListesi,
							"belgeBilgileri"  : belgeBilgileri,
						}
						return JsonResponse(context)
						
				cariHareketleri = []

				for fatura in Fatura.objects.all():
					faturaTipi = ""
					if fatura.FaturaTipi == "1":
						faturaTipi = "Satış Faturası"
					if fatura.FaturaTipi == "2":
						faturaTipi = "Alış Faturası"	
					cariHareketi = {"Hesap":"Fatura","id":fatura.id,"CariKodu":fatura.CariKodu,"Islem":faturaTipi,\
					"IslemNo":fatura.FaturaSeri+" "+str(fatura.FaturaSira),"IslemTarihi":fatura.IslemTarihi}
					cariHareketleri.append(cariHareketi)

				for irsaliye in Irsaliye.objects.all():
					irsaliyeTipi = ""
					if irsaliye.IrsaliyeTipi == "1":
						irsaliyeTipi = "Satış İrsaliyesi"
					if irsaliye.IrsaliyeTipi == "2":
						irsaliyeTipi = "Alış İrsaliyesi"
					cariHareketi = {"Hesap":"Irsaliye","id":irsaliye.id,"CariKodu":irsaliye.CariKodu,"Islem":irsaliyeTipi,\
					"IslemNo":irsaliye.IrsaliyeNo,"IslemTarihi":irsaliye.SevkTarihi}
					cariHareketleri.append(cariHareketi)
					
				for siparis in Siparis.objects.all():
					siparisTipi = ""
					if siparis.SiparisTipi == "1":
						siparisTipi = "Verilen Sipariş"
					if siparis.SiparisTipi == "2":
						siparisTipi = "Alınan Sipariş"
					cariHareketi = {"Hesap":"Siparis","id":siparis.id,"CariKodu":siparis.CariKodu,"Islem":siparisTipi,\
					"IslemNo":siparis.SiparisFisiNo,"IslemTarihi":siparis.SiparisTarihi}
					cariHareketleri.append(cariHareketi)		

				for banka in BankaHareketleri.objects.all():
					if(banka.CariKodu != "" and banka.CariKodu != None):
						dekontTipi = ""
						if banka.Dekont == "1":
							dekontTipi = "Tahsilat Dekontu"
						if banka.Dekont == "2":
							dekontTipi = "Tediye Dekontu"
						cariHareketi = {"Hesap":"Banka","id":banka.id,"CariKodu":banka.CariKodu,"Islem":dekontTipi,\
						"IslemNo":banka.DekontNo,"IslemTarihi":banka.DekontTarihi}
						cariHareketleri.append(cariHareketi)			

				for kasa in KasaHareketleri.objects.all():
					if(kasa.CariKodu != "" and kasa.CariKodu != None):
						makbuzTipi = ""
						if kasa.Makbuz == "1":
							makbuzTipi = "Tahsilat Makbuzu"
						if kasa.Makbuz == "2":
							makbuzTipi = "Tediye Makbuzu"
						cariHareketi = {"Hesap":"Kasa","id":kasa.id,"CariKodu":kasa.CariKodu,"Islem":makbuzTipi,\
						"IslemNo":kasa.MakbuzNo,"IslemTarihi":kasa.MakbuzTarihi}
						cariHareketleri.append(cariHareketi)	

				for cekler in Cek.objects.all():
					tipi = ""
					if cekler.Tipi == "1":
						tipi = "Çek Giriş(Alınan Çek)"
					if cekler.Tipi == "2":
						tipi = "Çek Çıkış(Cari Hesaba)"
					if cekler.Tipi == "3":
						tipi = "Çek Çıkış(Banka Tahsil)"
					if cekler.Tipi == "4":
						tipi = "Çek Çıkış(Banka Teminat)"
					
					cariHareketi = {"Hesap":"Cek","id":cekler.id,"CariKodu":cekler.CariKodu,"Islem":tipi,\
					"IslemNo":cekler.CekNo,"IslemTarihi":cekler.BordroTarihi}
					cariHareketleri.append(cariHareketi)
	
				for senet in Senet.objects.all():
					tipi = ""
					if senet.Tipi == "1":
						tipi = "Senet Giriş(Alınan Senet)"
					if senet.Tipi == "2":
						tipi = "Senet Çıkış(Cari Hesaba)"
					if senet.Tipi == "3":
						tipi = "Senet Çıkış(Banka Tahsil)"
					if senet.Tipi == "4":
						tipi = "Senet Çıkış(Banka Teminat)"			
					cariHareketi = {"Hesap":"Senet","id":senet.id,"CariKodu":senet.CariKodu,"Islem":tipi,\
					"IslemNo":senet.SenetNo,"IslemTarihi":senet.BordroTarihi}
					cariHareketleri.append(cariHareketi)	
							
				context = {
					"modulYetkisi"    : modulYetkisi,
					"islemlerKontrol" : islemlerKontrol,
					"cariHareketleri" : cariHareketleri,
				}
				return render (request, "cari/carihareketleri.html",context)
			else:		
				messages.success(request, "Cari Hareketleri Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")