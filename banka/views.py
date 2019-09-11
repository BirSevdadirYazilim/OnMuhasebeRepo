from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from kasa.models import *
from cari.models import *
from fatura.models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

suan = timezone.now()
def BankaOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsBanka == True):
			islemlerKontrol = get_object_or_404(BankaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsBankaOlustur == True):
				if request.is_ajax():	
					ajaxBankaKodu 	        = request.POST.get("ajaxBankaKodu")
					ajaxBankaAdi            = request.POST.get("ajaxBankaAdi")
					ajaxBankaSube           = request.POST.get("ajaxBankaSube")
					ajaxBankaIl             = request.POST.get("ajaxBankaIl")
					ajaxBankaIlce           = request.POST.get("ajaxBankaIlce")
					ajaxBankaAcilisBakiyesi = request.POST.get("ajaxBankaAcilisBakiyesi")
					ajaxBankaAdres          = request.POST.get("ajaxBankaAdres")
					ajaxBankaTel1           = request.POST.get("ajaxBankaTel1")
					ajaxBankaTel2           = request.POST.get("ajaxBankaTel2")
					ajaxBankaHesapNo        = request.POST.get("ajaxBankaHesapNo")
					ajaxBankaIbanNo         = request.POST.get("ajaxBankaIbanNo")
					ajaxBankaYetkilisi      = request.POST.get("ajaxBankaYetkilisi")
					ajaxBankaAcilisTarihi   = request.POST.get("ajaxBankaAcilisTarihi") 	
					if(ajaxBankaKodu != "" and ajaxBankaAdi != "" and ajaxBankaSube != "" and ajaxBankaIl != "" and ajaxBankaIlce != "" and ajaxBankaAcilisBakiyesi != "" and ajaxBankaAdres != "" and ajaxBankaTel1 != "" and ajaxBankaHesapNo != "" and ajaxBankaIbanNo != "" and ajaxBankaAcilisTarihi != ""):
						# Banka Kodu Mükerrer Kontrolu
						try:
							bankaKoduKontrol = get_object_or_404(Banka,BankaKodu=ajaxBankaKodu)
							context = {"ajaxMesaj" : "Bu Banka Kodu Kullanılıyor !"}
							return JsonResponse(context)
						except:
							pass
						# Banka Adı Mükerrer Kontrolu
						try:
							bankaAdiKontrol = get_object_or_404(Banka,BankaAdi=ajaxBankaAdi)
							context = {"ajaxMesaj" : "Bu Banka Adı Kullanılıyor !"}
							return JsonResponse(context)
						except:
							pass
						sqlBanka = Banka()
						sqlBanka.BankaKodu           = ajaxBankaKodu
						sqlBanka.BankaAdi            = ajaxBankaAdi
						sqlBanka.BankaSube           = ajaxBankaSube
						sqlBanka.BankaAcilisBakiyesi = ajaxBankaAcilisBakiyesi
						sqlBanka.BankaBorc           = ajaxBankaAcilisBakiyesi
						sqlBanka.BankaAlacak         = 0
						sqlBanka.BankaAdres          = ajaxBankaAdres
						sqlBanka.BankaIl             = ajaxBankaIl
						sqlBanka.BankaIlce           = ajaxBankaIlce
						sqlBanka.BankaTel1           = ajaxBankaTel1
						sqlBanka.BankaTel2 	         = ajaxBankaTel2
						sqlBanka.BankaHesapNo        = ajaxBankaHesapNo
						sqlBanka.BankaIbanNo         = ajaxBankaIbanNo 
						sqlBanka.BankaYetkilisi      = ajaxBankaYetkilisi
						sqlBanka.BankaAcilisTarihi   = ajaxBankaAcilisTarihi
						sqlBanka.BankaKaydiOlusturan = request.session["KullaniciKodu"]
						sqlBanka.save()
						if(ajaxBankaAcilisBakiyesi == None):
							ajaxBankaAcilisBakiyesi = 0
							replaceAjaxBankaAcilisBakiyesi = 0
						else:
							replaceAjaxBankaAcilisBakiyesi = ajaxBankaAcilisBakiyesi.replace(",",".")
						bankaHareketlerOlustur = BankaHareketleri()
						bankaHareketlerOlustur.BankaKodu     = ajaxBankaKodu
						bankaHareketlerOlustur.Dekont        = "3"
						bankaHareketlerOlustur.DekontNo      = ""
						bankaHareketlerOlustur.DekontTarihi  = ajaxBankaAcilisTarihi
						bankaHareketlerOlustur.BankaBorc     = float(replaceAjaxBankaAcilisBakiyesi)
						bankaHareketlerOlustur.BankaAlacak   = 0
						bankaHareketlerOlustur.Aciklama      = "Açılış"
						bankaHareketlerOlustur.save()
						ajaxMesaj = "1"
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
					context = {"ajaxMesaj" : ajaxMesaj,}
					return JsonResponse(context)
				context = {
					"suan" 	       : suan,
					"modulYetkisi" : modulYetkisi,
				}
				return render (request, "banka/olustur.html", context)
			else:		
				messages.success(request, "Banka Kaydı Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")		
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")				
	
def BankaListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsBanka == True):
			islemlerKontrol = get_object_or_404(BankaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsBankaListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlBanka = get_object_or_404(Banka, id=ajaxDetay)
						context = {
							"ajaxBankaKodu"            : sqlBanka.BankaKodu,
							"ajaxBankaAdi"             : sqlBanka.BankaAdi,
							"ajaxBankaAcilisBakiyesi"  : sqlBanka.BankaAcilisBakiyesi,
							"ajaxBankaIl"              : sqlBanka.BankaIl,
							"ajaxBankaIlce"            : sqlBanka.BankaIlce,
							"ajaxBankaAdres"           : sqlBanka.BankaAdres,
							"ajaxBankaBorc"            : sqlBanka.BankaBorc,
							"ajaxBankaAlacak"          : sqlBanka.BankaAlacak,
							"ajaxBankaTel1"            : sqlBanka.BankaTel1,
							"ajaxBankaTel2"            : sqlBanka.BankaTel2,
							"ajaxBankaHesapNo"         : sqlBanka.BankaHesapNo,
							"ajaxBankaIbanNo"          : sqlBanka.BankaIbanNo,
							"ajaxBankaYetkilisi"       : sqlBanka.BankaYetkilisi,
							"ajaxBankaAcilisTarihi"    : sqlBanka.BankaAcilisTarihi,
							"ajaxBankaKaydiOlusturan"  : sqlBanka.BankaKaydiOlusturan,
							"ajaxBankaDuzenlemeTarihi" : sqlBanka.BankaDuzenlemeTarihi,
							"ajaxBankaKaydıDuzenleyen" : sqlBanka.BankaKaydıDuzenleyen,
						}
						return JsonResponse(context)

					ajaxGuncelle = request.POST.get("ajaxGuncelle")	
					if(ajaxGuncelle):
						sqlBankaGuncelle = get_object_or_404(Banka, id=ajaxGuncelle)
						context = {
							"ajaxId"      				 : sqlBankaGuncelle.id,
							"ajaxBankaAdresGuncelle"     : sqlBankaGuncelle.BankaAdres,
							"ajaxBankaTel1Guncelle"      : sqlBankaGuncelle.BankaTel1,
							"ajaxBankaTel2Guncelle"      : sqlBankaGuncelle.BankaTel2,
							"ajaxBankaHesapNoGuncelle"   : sqlBankaGuncelle.BankaHesapNo,
							"ajaxBankaIbanNoGuncelle"    : sqlBankaGuncelle.BankaIbanNo,
							"ajaxBankaYetkilisiGuncelle" : sqlBankaGuncelle.BankaYetkilisi,
						}
						return JsonResponse(context)

					ajaxIdGuncelle             = request.POST.get("ajaxIdGuncelle")
					ajaxBankaAdresGuncelle     = request.POST.get("ajaxBankaAdresGuncelle")
					ajaxBankaTel1Guncelle      = request.POST.get("ajaxBankaTel1Guncelle")
					ajaxBankaTel2Guncelle      = request.POST.get("ajaxBankaTel2Guncelle")
					ajaxBankaHesapNoGuncelle   = request.POST.get("ajaxBankaHesapNoGuncelle")
					ajaxBankaIbanNoGuncelle    = request.POST.get("ajaxBankaIbanNoGuncelle")
					ajaxBankaYetkilisiGuncelle = request.POST.get("ajaxBankaYetkilisiGuncelle")	
					if(ajaxIdGuncelle):
						sqlBankaKaydet = get_object_or_404(Banka, id=ajaxIdGuncelle)
						sqlBankaKaydet.BankaAdres           = ajaxBankaAdresGuncelle
						sqlBankaKaydet.BankaTel1            = ajaxBankaTel1Guncelle
						sqlBankaKaydet.BankaTel2            = ajaxBankaTel2Guncelle
						sqlBankaKaydet.BankaHesapNo         = ajaxBankaHesapNoGuncelle
						sqlBankaKaydet.BankaIbanNo          = ajaxBankaIbanNoGuncelle
						sqlBankaKaydet.BankaYetkilisi       = ajaxBankaYetkilisiGuncelle
						sqlBankaKaydet.BankaDuzenlemeTarihi = suan
						sqlBankaKaydet.BankaKaydıDuzenleyen = request.session["KullaniciKodu"]
						sqlBankaKaydet.save()
						context = {"ajaxMesaj" : "Başarıyla Güncellendi !"}
						return JsonResponse(context)	

					ajaxSil = request.POST.get("ajaxSil")	
					if(ajaxSil):
						sqlBankaSil = get_object_or_404(Banka, id=ajaxSil)
						sqlBankaSil.IsDeleted = True
						sqlBankaSil.save()
						context = {"ajaxMesaj" : "Başarıyla Silindi !"}
						return JsonResponse(context)	
	
				sqlBanka = Banka.objects.filter(IsDeleted=False)
				bakiyeList = []
				for x in sqlBanka:
					bakiyeDemet = {"BankaId":x.id,"BankaAdi":x.BankaAdi,"BankaAcilisBakiyesi":x.BankaAcilisBakiyesi,\
					"BankaBorc":x.BankaBorc,"BankaAlacak":x.BankaAlacak,\
					"BankaBakiyesi":x.BankaBorc - x.BankaAlacak}
					bakiyeList.append(bakiyeDemet)
				context = {
					"modulYetkisi"    : modulYetkisi,
					"bakiyeList"      : bakiyeList,
					"islemlerKontrol" : islemlerKontrol
				}
				return render (request, "banka/listele.html", context)
			else:		
				messages.success(request, "Banka Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")			
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def BankaHareketleriOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsBanka == True):
			islemlerKontrol = get_object_or_404(BankaHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsBankaHareketleriOlustur == True):
				if request.is_ajax():
					ajaxDekontNoKontrol      = request.POST.get("ajaxDekontNoKontrol")
					ajaxBankaDekontNoKontrol = request.POST.get("ajaxBankaDekontNoKontrol")
					if(ajaxDekontNoKontrol and ajaxBankaDekontNoKontrol):
						dekontNo = None
						try:
							sqlDekontNo = get_object_or_404(DekontNo,BankaKodu=ajaxBankaDekontNoKontrol)
							if(ajaxDekontNoKontrol == "1"):
								if(sqlDekontNo.TahsilatDekontuNo != ""):
									dekontNo = sqlDekontNo.TahsilatDekontuNo
								else:
									dekontNo = None
							if(ajaxDekontNoKontrol == "2"):
								if(sqlDekontNo.TediyeDekontuNo != ""):
									dekontNo = sqlDekontNo.TediyeDekontuNo
								else:
									dekontNo = None
						except:
							dekontNo = None
						context = {"ajaxSqlDekontNo" : dekontNo,}
						return JsonResponse(context)
		
					ajaxBakiyeKontrol   = request.POST.get("ajaxBakiyeKontrol")
					ajaxBankaAdiKontrol	= request.POST.get("ajaxBankaAdiKontrol")
					if(ajaxBakiyeKontrol != None):
						replaceBakiyeKontrol = ajaxBakiyeKontrol.replace(",",".")
						sqlBankaAdi = get_object_or_404(Banka,BankaKodu=ajaxBankaAdiKontrol)
						if(float(sqlBankaAdi.BankaBorc - sqlBankaAdi.BankaAlacak) - float(replaceBakiyeKontrol) < 0):
							context = {"ajaxMesaj" : "Yetersiz Bakiye !"}
						else:
							context = {"ajaxMesaj" : ""}
						return JsonResponse(context)	
					ajaxBankaAdi     = request.POST.get("ajaxBankaAdi")
					ajaxDekont       = request.POST.get("ajaxDekont")
					ajaxDekontNo     = request.POST.get("ajaxDekontNo")
					ajaxDekontTarihi = request.POST.get("ajaxDekontTarihi")
					ajaxTutar        = request.POST.get("ajaxTutar")
					ajaxAciklama     = request.POST.get("ajaxAciklama")
					ajaxCariUnvani   = request.POST.get("ajaxCariUnvani")		
					if(ajaxBankaAdi != "" and ajaxDekont != "" and ajaxDekontNo != "" and ajaxDekontTarihi != "" and ajaxTutar != "" and ajaxCariUnvani != ""):
						replaceTutar = ajaxTutar.replace(",",".")
						bankaHareketlerOlustur = BankaHareketleri()
						bankaHareketlerOlustur.BankaKodu     = ajaxBankaAdi
						bankaHareketlerOlustur.Dekont        = ajaxDekont
						bankaHareketlerOlustur.DekontNo      = ajaxDekontNo
						bankaHareketlerOlustur.DekontTarihi  = ajaxDekontTarihi
						if(ajaxDekont == "1"):
							bankaHareketlerOlustur.BankaBorc   = float(replaceTutar)
						if(ajaxDekont == "2"):
							bankaHareketlerOlustur.BankaAlacak = float(replaceTutar)	
						bankaHareketlerOlustur.Aciklama      = ajaxAciklama
						bankaHareketlerOlustur.CariKodu    	 = ajaxCariUnvani
						bankaHareketlerOlustur.save()
						ajaxMesaj = "1"
						# Seçilen Dekonto Göre Dekont Numarasını DekontNo Tablosundunda Arttırma
						try:
							sqlDekontNoGuncelle = get_object_or_404(DekontNo,BankaKodu=ajaxBankaAdi)
							if(ajaxDekont == "1"):
								sqlDekontNoGuncelle.TahsilatDekontuNo = int(ajaxDekontNo) + 1
								sqlDekontNoGuncelle.save()
							if(ajaxDekont == "2"):	
								sqlDekontNoGuncelle.TediyeDekontuNo = int(ajaxDekontNo) + 1
								sqlDekontNoGuncelle.save()
						except:
							pass
						# Seçilen Dekonta Göre Banka Bakiyesini Güncelleme		
						try:
							bankaGuncelle = get_object_or_404(Banka,BankaKodu=ajaxBankaAdi)
							if(ajaxDekont == "1"):
								bankaGuncelle.BankaBorc = float(bankaGuncelle.BankaBorc) + float(replaceTutar)
								bankaGuncelle.save()
							if(ajaxDekont == "2"):
								bankaGuncelle.BankaAlacak = float(bankaGuncelle.BankaAlacak) + float(replaceTutar)
								bankaGuncelle.save()
						except:
							pass
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
					context = {"ajaxMesaj": ajaxMesaj}
					return JsonResponse(context)
				sqlCari  = Cari.objects.filter(IsDeleted=False)
				sqlBanka = Banka.objects.filter(IsDeleted=False)
				context = {
					"modulYetkisi" : modulYetkisi,
					"suan"         : suan,
					"sqlCari"	   : sqlCari,
					"sqlBanka"     : sqlBanka,
				}
				return render (request, "banka/bankaharolustur.html", context)
			else:		
				messages.success(request, "Banka Hareketleri Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def BankaHareketleriListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsBanka == True):
			islemlerKontrol = get_object_or_404(BankaHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsBankaHareketleriListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlBankaHareketleri = get_object_or_404(BankaHareketleri, id=ajaxDetay)
						if(sqlBankaHareketleri.Dekont == "1"):
							varDekont = "Tahsilat Dekontu"
						if(sqlBankaHareketleri.Dekont == "2"):
							varDekont = "Tediye Dekontu"
						if(sqlBankaHareketleri.Dekont == "3"):
							varDekont = "Banka Açılış Fişi"		
						context = {
							"ajaxCariUnvani"   : sqlBankaHareketleri.CariKodu,
							"ajaxBankaKodu"    : sqlBankaHareketleri.BankaKodu,
							"ajaxDekont"       : varDekont,
							"ajaxDekontNo"     : sqlBankaHareketleri.DekontNo,
							"ajaxDekontTarihi" : sqlBankaHareketleri.DekontTarihi,
							"ajaxBankaBorc"    : sqlBankaHareketleri.BankaBorc,
							"ajaxBankaAlacak"  : sqlBankaHareketleri.BankaAlacak,
						}
						return JsonResponse(context)
					ajaxIptal = request.POST.get("ajaxIptal")
					if(ajaxIptal):
						sqlBankaHareketleriIptal = get_object_or_404(BankaHareketleri, id=ajaxIptal)
						sqlBankaHareketleriIptal.IsCanceled = True
						sqlBankaHareketleriIptal.save()
						try:
							bankaGuncelle = get_object_or_404(Banka, BankaKodu=sqlBankaHareketleriIptal.BankaKodu)
							if(sqlBankaHareketleriIptal.Dekont == "1"):
								bankaGuncelle.BankaBorc = float(bankaGuncelle.BankaBorc) - float(sqlBankaHareketleriIptal.BankaBorc)
								bankaGuncelle.save()
							if(sqlBankaHareketleriIptal.Dekont == "2"):
								bankaGuncelle.BankaAlacak = float(bankaGuncelle.BankaAlacak) - float(sqlBankaHareketleriIptal.BankaAlacak)
								bankaGuncelle.save()
						except:
							pass
						# BAT = Bankalarlar Arası Transfer	
						try:
							bankaGuncelleBAT = get_object_or_404(Banka, BankaKodu=sqlBankaHareketleriIptal.CariKodu)
							if(sqlBankaHareketleriIptal.Dekont == "1"):
								bankaGuncelleBAT.BankaAlacak = float(bankaGuncelleBAT.BankaAlacak) - float(sqlBankaHareketleriIptal.BankaBorc)
								bankaGuncelleBAT.save()
							if(sqlBankaHareketleriIptal.Dekont == "2"):
								bankaGuncelleBAT.BankaBorc = float(bankaGuncelleBAT.BankaBorc) - float(sqlBankaHareketleriIptal.BankaAlacak)
								bankaGuncelleBAT.save()
						except:
							pass
						context = {"ajaxMesaj" : "Başarılı"}
						return JsonResponse(context)
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						sqlBankaHareketleriSil = get_object_or_404(BankaHareketleri, id=ajaxSil)
						sqlBankaHareketleriSil.IsDeleted = True
						sqlBankaHareketleriSil.save()
						context = {"ajaxMesaj"   : "Başarılı"}
						return JsonResponse(context)		
				sqlBankaHareketleri = BankaHareketleri.objects.filter(IsCanceled=False)
				sqlBankaHareketleriIsCanceled = BankaHareketleri.objects.filter(IsCanceled=True,IsDeleted=False)
				context = {
					"modulYetkisi" 					: modulYetkisi,
					"islemlerKontrol" 				: islemlerKontrol,
					"sqlBankaHareketler" 			: sqlBankaHareketleri,
					"sqlBankaHareketleriIsCanceled" : sqlBankaHareketleriIsCanceled,
				}
				return render (request, "banka/bankahareketleri.html", context)
			else:		
				messages.success(request, "Banka Hareketleri Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def HesaplarArasiTransfer(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsBanka == True):
			islemlerKontrol = get_object_or_404(BankaHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsBankaHareketleriOlustur == True):
				if request.is_ajax():
					ajaxDekontKontrol = request.POST.get("ajaxDekontKontrol")
					ajaxTahDekNoBanka = request.POST.get("ajaxTahDekNoBanka")
					ajaxTedDekNoBanka = request.POST.get("ajaxTedDekNoBanka")
					if(ajaxDekontKontrol):
						if(ajaxDekontKontrol == "1"):
							dekontNo = ""
							try:
								sqlBankaKontrol = get_object_or_404(Banka,BankaKodu=ajaxTahDekNoBanka)
								try:
									sqlDekontNo = get_object_or_404(DekontNo,BankaKodu=ajaxTahDekNoBanka)
									if(sqlDekontNo.TahsilatDekontuNo != ""):
										dekontNo = sqlDekontNo.TahsilatDekontuNo
									else:
										dekontNo = None
								except:
									dekontNo = None					
							except:
								dekontNo = False
							context = {"ajaxSqlDekontNo" : dekontNo,}
							return JsonResponse(context)
						if(ajaxDekontKontrol == "2"):
							dekontNo = ""
							try:
								sqlBankaKontrol = get_object_or_404(Banka,BankaKodu=ajaxTedDekNoBanka)
								try:
									sqlTedDekNo = get_object_or_404(DekontNo,BankaKodu=ajaxTedDekNoBanka)
									if(sqlTedDekNo.TediyeDekontuNo != ""):
										dekontNo = sqlTedDekNo.TediyeDekontuNo
									else:
										dekontNo = None
								except:
									dekontNo = None
							except:
									dekontNo = False		
							context = {"ajaxSqlDekontNo" : dekontNo,}
							return JsonResponse(context)

					#Seçilen Dekonta Göre DokontNo Tablosundan Dekont Seçimi
					if(ajaxDekontKontrol == "1"):
						tahDekNo = ""
						try:
							sqlDekontNo = get_object_or_404(DekontNo,BankaKodu=ajaxBankaDekontKontrol)
							if(sqlDekontNo.TahsilatDekontuNo != ""):
								tahDekNo = sqlDekontNo.TahsilatDekontuNo
							else:
								tahDekNo = None	
						except:
							tahDekNo = None
						key = "1"
						context = {
							"sqlTahsilatDekontNo" : tahDekNo,
						    "ajaxKey"             : key,
						}
						return JsonResponse(context)
					if(ajaxDekontKontrol == "2"):
						tedDekNo = ""
						try:
							sqlDekontNo = get_object_or_404(DekontNo,BankaKodu=ajaxBankaDekontKontrol)
							if(sqlDekontNo.TediyeDekontuNo != ""):
								tedDekNo = sqlDekontNo.TediyeDekontuNo
							else:
								tedDekNo = None
						except:
							tedDekNo = None
						key = "2"
						context = {
							"sqlTediyeDekontNo" : tedDekNo,
						    "ajaxKey"           : key,
						}
						return JsonResponse(context)

					ajaxBakiyeKontrol    = request.POST.get("ajaxBakiyeKontrol")
					ajaxBankaKoduKontrol = request.POST.get("ajaxBankaKoduKontrol")
					# Tediye Dekontu Seçilirse Para Çıkışının Yapılacağı Hesepta Yeterli Bakiye Olup Olmadığı Kontrolu 
					if(ajaxBakiyeKontrol):
						replaceBakiyeKontrol = ajaxBakiyeKontrol.replace(",",".")	
						sqlBankaAdi = get_object_or_404(Banka,BankaKodu=ajaxBankaKoduKontrol)
						
						if(float(sqlBankaAdi.BankaBorc - sqlBankaAdi.BankaAlacak) - float(replaceBakiyeKontrol) < 0):
							context = {"ajaxMesaj" : "Yetersiz Bakiye !",}	
						else:
							context = {"ajaxMesaj" : ""}	
						return JsonResponse(context)
							
					ajaxBorcHesabi    = request.POST.get("ajaxBorcHesabi")	
					ajaxAlacakHesabi  = request.POST.get("ajaxAlacakHesabi")
					ajaxDekont        = request.POST.get("ajaxDekont")
					ajaxDekontNo      = request.POST.get("ajaxDekontNo")
					ajaxDekontTarihi  = request.POST.get("ajaxDekontTarihi")
					ajaxTutar         = request.POST.get("ajaxTutar")
					ajaxAciklama      = request.POST.get("ajaxAciklama")
					if(ajaxBorcHesabi != "" and ajaxAlacakHesabi != "" and ajaxDekont != "" and ajaxDekontNo != "" and ajaxTutar != "" and ajaxDekontTarihi != ""):
						replaceTutar = ajaxTutar.replace(",",".")
						if(ajaxDekont == "1"):
							try:
								tedDekNoOto = get_object_or_404(DekontNo,BankaKodu=ajaxAlacakHesabi)
								if(tedDekNoOto.TediyeDekontuNo != "" or tedDekNoOto.TediyeDekontuNo != None):
									virmanBorc = BankaHareketleri()
									virmanBorc.BankaKodu     = ajaxBorcHesabi
									virmanBorc.Dekont        = ajaxDekont
									virmanBorc.DekontNo      = ajaxDekontNo
									virmanBorc.DekontTarihi  = ajaxDekontTarihi
									virmanBorc.BankaBorc     = float(replaceTutar)
									virmanBorc.Aciklama      = ajaxAciklama
									virmanBorc.CariKodu      = ajaxAlacakHesabi
									virmanBorc.save()
									virmanAlacakOto = BankaHareketleri()
									virmanAlacakOto.BankaKodu     = ajaxAlacakHesabi
									virmanAlacakOto.Dekont        = "2"
									virmanAlacakOto.DekontNo      = tedDekNoOto.TediyeDekontuNo
									virmanAlacakOto.DekontTarihi  = ajaxDekontTarihi
									virmanAlacakOto.BankaAlacak   = float(replaceTutar)
									virmanAlacakOto.Aciklama      = "Ödeme Yapıldı"
									virmanAlacakOto.CariKodu      = ajaxBorcHesabi
									virmanAlacakOto.save()
									tedDekNoOto.TediyeDekontuNo = int(tedDekNoOto.TediyeDekontuNo) + 1
									tedDekNoOto.save()
									ajaxMesaj = "1"
									try:
										sqlTahDekNoGuncelle = get_object_or_404(DekontNo,BankaKodu=ajaxBorcHesabi)
										sqlTahDekNoGuncelle.TahsilatDekontuNo = int(ajaxDekontNo) + 1
										sqlTahDekNoGuncelle.save()
									except:
										pass
									try:
										bankaGuncelleBorc = get_object_or_404(Banka,BankaKodu=ajaxBorcHesabi)
										bankaGuncelleBorc.BankaBorc = float(bankaGuncelleBorc.BankaBorc) + float(replaceTutar)
										bankaGuncelleBorc.save()
									except:
										pass
									try:
										bankaGuncelleAlacak = get_object_or_404(Banka,BankaKodu=ajaxAlacakHesabi)
										bankaGuncelleAlacak.BankaAlacak = float(bankaGuncelleAlacak.BankaAlacak) + float(replaceTutar)
										bankaGuncelleAlacak.save()
									except:
										pass
								else:
									ajaxMesaj = False
							except:
								ajaxMesaj = False
						if(ajaxDekont == "2"):
							try:
								tahDekNoOto = get_object_or_404(DekontNo,BankaKodu=ajaxBorcHesabi)
								if(tahDekNoOto.TahsilatDekontuNo != "" or tahDekNoOto.TahsilatDekontuNo != None):
									virmanAlacak = BankaHareketleri()
									virmanAlacak.BankaKodu     = ajaxAlacakHesabi
									virmanAlacak.Dekont        = ajaxDekont
									virmanAlacak.DekontNo      = ajaxDekontNo
									virmanAlacak.DekontTarihi  = ajaxDekontTarihi
									virmanAlacak.BankaAlacak   = float(replaceTutar)
									virmanAlacak.Aciklama      = ajaxAciklama
									virmanAlacak.CariKodu      = ajaxBorcHesabi
									virmanAlacak.save()
									virmanBorcOto = BankaHareketleri()
									virmanBorcOto.BankaKodu     = ajaxBorcHesabi
									virmanBorcOto.Dekont        = "1"
									virmanBorcOto.DekontNo      = tahDekNoOto.TahsilatDekontuNo
									virmanBorcOto.DekontTarihi  = ajaxDekontTarihi
									virmanBorcOto.BankaBorc     = float(replaceTutar)
									virmanBorcOto.Aciklama      = "Ödeme Alındı"
									virmanBorcOto.CariKodu      = ajaxAlacakHesabi
									virmanBorcOto.save()
									tahDekNoOto.TahsilatDekontuNo = int(tahDekNoOto.TahsilatDekontuNo) + 1
									tahDekNoOto.save()
									ajaxMesaj = "Başarılı Bir Şekilde Kaydedildi !"
									# Seçilen Dekonta Göre Dekont Numarasını DekontNo Tablosundan Arttırma
									try:
										sqlTedDekNoGuncelle = get_object_or_404(DekontNo,BankaKodu=ajaxAlacakHesabi)
										sqlTedDekNoGuncelle.TediyeDekontuNo = int(ajaxDekontNo) + 1
										sqlTedDekNoGuncelle.save()
									except:
										pass
									# Seçilen Dekonta Göre Dekont Numarasını DekontNo Tablosundan Arttırma
									#Banka Bakiye Güncelleme
									try:
										bankaGuncelleAlacak = get_object_or_404(Banka,BankaKodu=ajaxAlacakHesabi)
										bankaGuncelleAlacak.BankaAlacak = float(bankaGuncelleAlacak.BankaAlacak) + float(replaceTutar)
										bankaGuncelleAlacak.save()
									except:
										pass
									try:
										bankaGuncelleBorc = get_object_or_404(Banka,BankaKodu=ajaxBorcHesabi)
										bankaGuncelleBorc.BankaBorc = float(bankaGuncelleBorc.BankaBorc) + float(replaceTutar)
										bankaGuncelleBorc.save()
									except:
										pass	
									#Banka Bakiye Güncelleme
								else:
									ajaxMesaj = False
							except:
								ajaxMesaj = False		
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
					context = {
						"ajaxMesaj" : ajaxMesaj,
					}
					return JsonResponse(context)	
				sqlKasa = Kasa.objects.filter(IsDeleted=False)
				sqlBanka = Banka.objects.filter(IsDeleted=False)
				context = {
					"modulYetkisi" : modulYetkisi,
					"suan"		   : suan,
					"sqlBanka"     : sqlBanka,
					"sqlKasa" 	   : sqlKasa,
				}
				return render (request, "banka/transfer.html", context)
			else:		
				messages.success(request, "Banka Hareketleri Oluşturma Yetkiniz Yok !")
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
		if(modulYetkisi.IsBanka == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsBankaTanimlamalari == True):
				if request.is_ajax():
					ajaxBankaSecimi       = request.POST.get("ajaxBankaSecimi")
					if(ajaxBankaSecimi):
						try:
							sqlBankaDekontNo = get_object_or_404(DekontNo,BankaKodu=ajaxBankaSecimi)
							sqlTahDekNo = sqlBankaDekontNo.TahsilatDekontuNo
							sqlTedDekNo = sqlBankaDekontNo.TediyeDekontuNo
						except:
							sqlTahDekNo = "" 
							sqlTedDekNo   = ""
						context = {
							"ajaxBankaTahDek" : sqlTahDekNo,
							"ajaxBankaTedDek" : sqlTedDekNo,
							}
						return JsonResponse(context)
					ajaxBankaKodu         = request.POST.get("ajaxBankaKodu")
					ajaxTahsilatDekontuNo = request.POST.get("ajaxTahsilatDekontuNo")
					ajaxTediyeDekontuNo   = request.POST.get("ajaxTediyeDekontuNo")
					if(ajaxBankaKodu):
						try:
							sqlDekontNo = get_object_or_404(DekontNo,BankaKodu=ajaxBankaKodu)
							if request.is_ajax():
								if(ajaxTahsilatDekontuNo != ""):
									sqlDekontNo.TahsilatDekontuNo = ajaxTahsilatDekontuNo
									sqlDekontNo.save()
								if(ajaxTediyeDekontuNo != ""):
									sqlDekontNo.TediyeDekontuNo = ajaxTediyeDekontuNo
									sqlDekontNo.save()
								context = {"ajaxMesaj" : "Kayıt Başarılı !"}
								return JsonResponse(context)
						except:
							if request.is_ajax():
								sqlDekontNoOlustur = DekontNo()
								if(ajaxTahsilatDekontuNo != ""):
									sqlDekontNoOlustur.BankaKodu         = ajaxBankaKodu
									sqlDekontNoOlustur.TahsilatDekontuNo = ajaxTahsilatDekontuNo
									sqlDekontNoOlustur.save()
								if(ajaxTediyeDekontuNo != ""):
									sqlDekontNoOlustur.BankaKodu       = ajaxBankaKodu
									sqlDekontNoOlustur.TediyeDekontuNo = ajaxTediyeDekontuNo
									sqlDekontNoOlustur.save()
								context = {"ajaxMesaj" : "Kayıt Başarılı !"}
								return JsonResponse(context)
				bankalar = Banka.objects.all()
				context = {
					"modulYetkisi" : modulYetkisi,
					"bankalar"     : bankalar,
				}		
				return render (request, "banka/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")		