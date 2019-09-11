import random
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .encryption import encryption_h
from django.utils import timezone

suan = timezone.now()

liste = range(10)	
capce = ""
for i in random.sample(liste, 5):
	capce = capce + str(i)
	
def KullaniciGiris(request):
	request.session.clear()
	if request.is_ajax():
		ajaxKullaniciAdi    = request.POST.get("ajaxKullaniciAdi")
		ajaxKullaniciParola = request.POST.get("ajaxKullaniciParola")
		ajaxCapce 			= request.POST.get("ajaxCapce")
		if(ajaxCapce == capce):
			if (ajaxKullaniciAdi != "" and ajaxKullaniciParola != ""):
				encryptionParola = encryption_h(ajaxKullaniciAdi, ajaxKullaniciParola)
				try:
					sqlKullanicilar = get_object_or_404(Kullanicilar, KullaniciAdi=ajaxKullaniciAdi, KullaniciParola=encryptionParola)
					if(sqlKullanicilar.KullaniciDurumu == True):
						sqlKullanicilar.SonGiris = suan
						sqlKullanicilar.save()
						request.session["KullaniciKodu"] = sqlKullanicilar.KullaniciKodu
						request.session["KullaniciAdi"]  = sqlKullanicilar.KullaniciAdi
						ajaxMesaj = True
					if(sqlKullanicilar.KullaniciDurumu == False):
						ajaxMesaj = "Kullanıcı Pasifize Edilmiş !"	
				except:
					ajaxMesaj = "Böyle Bir Kullanici Yok !"	
			else:
				ajaxMesaj = "Kullanıcı Adı Ve Parola Boş Bırakılamaz !"
		else:
			ajaxMesaj = "Girmiş Olduğunuz Kod Doğrulanamadı !"
		context = {"ajaxMesaj" : ajaxMesaj}
		return JsonResponse(context)
	context = {
		"capce" : capce,
	}
	return render(request, "kullanicilar/giris.html", context)

def KullaniciCikis(request):
	request.session.clear()
	return redirect ("kullanicilar:giris")

def KullaniciKayit(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsKullanicilar == True):
			islemlerKontrol = get_object_or_404(KullaniciYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKullaniciOlustur == True):
				if request.is_ajax():
					ajaxKullaniciKodu 	 = request.POST.get("ajaxKullaniciKodu")
					ajaxKullaniciAdi 	 = request.POST.get("ajaxKullaniciAdi")
					ajaxKullaniciParola  = request.POST.get("ajaxKullaniciParola")
					ajaxKullaniciParolaD = request.POST.get("ajaxKullaniciParolaD")
					ajaxKullaniciTipi    = request.POST.get("ajaxKullaniciTipi")
					ajaxKullaniciGrubu   = request.POST.get("ajaxKullaniciGrubu")
					ajaxKullaniciDurumu  = request.POST.get("ajaxKullaniciDurumu")
					if(ajaxKullaniciKodu and ajaxKullaniciAdi and ajaxKullaniciParola and ajaxKullaniciParolaD and ajaxKullaniciTipi and ajaxKullaniciDurumu):	
						if(ajaxKullaniciParola == ajaxKullaniciParolaD):
							try:
								sqlKullanicilar = get_object_or_404(Kullanicilar, KullaniciKodu=ajaxKullaniciKodu)
								ajaxMesaj = "Kayıtlı Kullanıcı Kodu !"
								key = 0
							except:
								key = 1
							try:
								sqlKullanicilar = get_object_or_404(Kullanicilar, KullaniciAdi=ajaxKullaniciAdi)
								ajaxMesaj = "Kayıtlı Kullanıcı Adı !"
								key1 = 0
							except:
								key1 = 1	
							if(key and key1 == 1):
								encryptionParola = encryption_h(ajaxKullaniciAdi, ajaxKullaniciParola)
								sql = Kullanicilar()
								sql.KullaniciKodu    = ajaxKullaniciKodu
								sql.KullaniciAdi     = ajaxKullaniciAdi
								sql.KullaniciParola  = encryptionParola
								sql.KullaniciTipi    = ajaxKullaniciTipi
								sql.KullaniciGrubu   = ajaxKullaniciGrubu	
								sql.KullaniciDurumu  = ajaxKullaniciDurumu
								sql.KayitTarihi 	 = suan
								sql.KayitYapan 		 = 'request.session["KullaniciKodu"]'
								sql.save()
								ajaxMesaj = "1"
						else:
							ajaxMesaj = "Parolalar Eşleşmiyor !"
						context = {"ajaxMesaj" : ajaxMesaj}
						return JsonResponse(context)
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
						context = {"ajaxMesaj" : ajaxMesaj}
						return JsonResponse(context)		
				sqlKullaniciTipiModel = KullaniciTipiModel.objects.all()
				sqlKullaniciGrubuModel = KullaniciGrubuModel.objects.all()			
				context = {
					"modulYetkisi" 			 : modulYetkisi,
					"sqlKullaniciTipiModel"  : sqlKullaniciTipiModel,
					"sqlKullaniciGrubuModel" : sqlKullaniciGrubuModel,
				}
				return render(request, "kullanicilar/kayit.html",context)
			else:		
				messages.success(request, "Kullanıcı Oluşturma Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")					
def KullaniciListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsKullanicilar == True):
			islemlerKontrol = get_object_or_404(KullaniciYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKullaniciListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlKullanicilarDetay = get_object_or_404(Kullanicilar,KullaniciKodu=ajaxDetay)
						context = {
							"ajaxKullaniciKodu"   : sqlKullanicilarDetay.KullaniciKodu,
							"ajaxKullaniciAdi"    : sqlKullanicilarDetay.KullaniciAdi,
							"ajaxKullaniciTipi"   : sqlKullanicilarDetay.KullaniciTipi,
							"ajaxKullaniciGrubu"  : sqlKullanicilarDetay.KullaniciGrubu,
							"ajaxKullaniciDurumu" : sqlKullanicilarDetay.KullaniciDurumu,
							"ajaxSonGiris"        : sqlKullanicilarDetay.SonGiris,
							"ajaxKayitTarihi"     : sqlKullanicilarDetay.KayitTarihi,
							"ajaxKayitYapan"      : sqlKullanicilarDetay.KayitYapan,
							"ajaxDuzeltmeTarihi"  : sqlKullanicilarDetay.DuzeltmeTarihi,
							"ajaxDuzeltmeYapan"   : sqlKullanicilarDetay.DuzeltmeYapan,
						}
						return JsonResponse(context)
					ajaxGuncelle = request.POST.get("ajaxGuncelle")
					if(ajaxGuncelle):
						sqlKullanicilarGuncelle = get_object_or_404(Kullanicilar,KullaniciKodu=ajaxGuncelle)
						if(sqlKullanicilarGuncelle.KullaniciDurumu == True):
							varKullaniciDurumu = 1
						if(sqlKullanicilarGuncelle.KullaniciDurumu == False):
							varKullaniciDurumu = 0	
						context = {
							"ajaxKullaniciIdGuncelle"     : sqlKullanicilarGuncelle.id,
							"ajaxKullaniciKoduGuncelle"   : sqlKullanicilarGuncelle.KullaniciKodu,
							"ajaxKullaniciAdiGuncelle"    : sqlKullanicilarGuncelle.KullaniciAdi,
							"ajaxKullaniciTipiGuncelle"   : sqlKullanicilarGuncelle.KullaniciTipi,
							"ajaxKullaniciGrubuGuncelle"  : sqlKullanicilarGuncelle.KullaniciGrubu,
							"ajaxKullaniciDurumuGuncelle" : varKullaniciDurumu,
							"ajaxKullaniciParolaGuncelle" : sqlKullanicilarGuncelle.KullaniciParola,
						}
						return JsonResponse(context)

					ajaxKullaniciIdKaydet      = request.POST.get("ajaxKullaniciIdKaydet")	
					ajaxKullaniciKoduKaydet    = request.POST.get("ajaxKullaniciKoduKaydet")
					ajaxKullaniciAdiKaydet 	   = request.POST.get("ajaxKullaniciAdiKaydet")
					ajaxKullaniciParolaKaydet  = request.POST.get("ajaxKullaniciParolaKaydet")
					ajaxKullaniciParolaDKaydet = request.POST.get("ajaxKullaniciParolaDKaydet")
					ajaxKullaniciTipiKaydet    = request.POST.get("ajaxKullaniciTipiKaydet")
					ajaxKullaniciGrubuKaydet   = request.POST.get("ajaxKullaniciGrubuKaydet")
					ajaxKullaniciDurumuKaydet  = request.POST.get("ajaxKullaniciDurumuKaydet")
					if(ajaxKullaniciIdKaydet):
						if(ajaxKullaniciKoduKaydet and ajaxKullaniciAdiKaydet and ajaxKullaniciParolaKaydet and ajaxKullaniciParolaDKaydet and ajaxKullaniciTipiKaydet and ajaxKullaniciDurumuKaydet):
							if(ajaxKullaniciParolaKaydet == ajaxKullaniciParolaDKaydet):
								encryptionPassword = encryption_h(ajaxKullaniciAdiKaydet, ajaxKullaniciParolaKaydet)
								sqlKaydet = get_object_or_404(Kullanicilar,id=ajaxKullaniciIdKaydet)
								sqlKaydet.KullaniciKodu   = ajaxKullaniciKoduKaydet
								sqlKaydet.KullaniciAdi 	  = ajaxKullaniciAdiKaydet
								sqlKaydet.KullaniciParola = encryptionPassword
								sqlKaydet.KullaniciTipi   = ajaxKullaniciTipiKaydet
								sqlKaydet.KullaniciGrubu  = ajaxKullaniciGrubuKaydet
								sqlKaydet.KullaniciDurumu = ajaxKullaniciDurumuKaydet
								sqlKaydet.DuzeltmeTarihi  = suan
								sqlKaydet.DuzeltmeYapan   = request.session["KullaniciKodu"]
								sqlKaydet.save()
								ajaxMesaj = "1"
							else:
								ajaxMesaj = "Parolalar Eşleşmiyor !"
							context = {"ajaxMesaj" : ajaxMesaj}
							return JsonResponse(context)
						else:
							ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
							context = {"ajaxMesaj" : ajaxMesaj}
							return JsonResponse(context)	
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						sqlKullanicilarSil = get_object_or_404(Kullanicilar,KullaniciKodu=ajaxSil)
						sqlKullanicilarSil.IsDeleted = True
						sqlKullanicilarSil.save()
						context = {"ajaxMesaj":"Silme İşlemi Başarılı !",}
						return JsonResponse(context)				
				sqlKullanicilar = Kullanicilar.objects.filter(IsDeleted=False)
				sqlKullaniciTipi = KullaniciTipiModel.objects.all()
				sqlKullaniciGrubu = KullaniciGrubuModel.objects.all()
				context = {
					"modulYetkisi"      : modulYetkisi,
					"islemlerKontrol"   : islemlerKontrol,
					"sqlKullanicilar"   : sqlKullanicilar,
					"sqlKullaniciTipi"  : sqlKullaniciTipi,
					"sqlKullaniciGrubu" : sqlKullaniciGrubu,
				}
				return render (request, "kullanicilar/listele.html", context)
			else:		
				messages.success(request, "Kullanıcı Listesini Görüntüleme Yetkiniz Yok !")
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
		if (modulYetkisi.IsKullanicilar == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKullaniciTanimlamalari == True):
				if request.is_ajax():
					ajaxKullaniciGrubuKodu = request.POST.get("ajaxKullaniciGrubuKodu")
					ajaxKullaniciGrubu     = request.POST.get("ajaxKullaniciGrubu")
					if(ajaxKullaniciGrubu):
						sqlKullaniciTanimlamalari = KullaniciGrubuModel()
						sqlKullaniciTanimlamalari.KullaniciGrubuKodu = ajaxKullaniciGrubuKodu
						sqlKullaniciTanimlamalari.KullaniciGrubu     = ajaxKullaniciGrubu
						sqlKullaniciTanimlamalari.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)

					ajaxKullaniciTipleri = request.POST.get("ajaxKullaniciTipleri")
					if(ajaxKullaniciTipleri):
						sqlModulYetkileri  = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						modulYetkileriList = []
						if(sqlModulYetkileri.IsAnaSayfa == True):
							modulYetkileriList.append("Anasayfa")
						if(sqlModulYetkileri.IsCari == True):
							modulYetkileriList.append("Cari")
						if(sqlModulYetkileri.IsKasa == True):
							modulYetkileriList.append("Kasa")
						if(sqlModulYetkileri.IsBanka == True):
							modulYetkileriList.append("Banka")
						if(sqlModulYetkileri.IsCekSenet == True):
							modulYetkileriList.append("ÇekSenet")
						if(sqlModulYetkileri.IsSiparis == True):
							modulYetkileriList.append("Sipariş")
						if(sqlModulYetkileri.IsFatura == True):
							modulYetkileriList.append("Fatura")
						if(sqlModulYetkileri.IsIrsaliye == True):
							modulYetkileriList.append("İrsaliye")
						if(sqlModulYetkileri.IsStok == True):
							modulYetkileriList.append("Stok")
						if(sqlModulYetkileri.IsKullanicilar == True):
							modulYetkileriList.append("Kullanıcılar")
						if(sqlModulYetkileri.IsTanimlamalar == True):
							modulYetkileriList.append("Tanımlamalar")									
						
						sqlKullaniciYetkileri  = get_object_or_404(KullaniciYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						kullaniciYetkileriList = []
						if(sqlKullaniciYetkileri.IsKullaniciOlustur == True):
							kullaniciYetkileriList.append("Kullanıcı Oluştur")
						if(sqlKullaniciYetkileri.IsKullaniciListele == True):
							kullaniciYetkileriList.append("Kullanıcı Listele")
						if(sqlKullaniciYetkileri.IsKullaniciDetay == True):
							kullaniciYetkileriList.append("Kullanıcı Detay")
						if(sqlKullaniciYetkileri.IsKullaniciGuncelle == True):
							kullaniciYetkileriList.append("Kullanıcı Güncelle")
						if(sqlKullaniciYetkileri.IsKullaniciSil == True):
							kullaniciYetkileriList.append("Kullanıcı Sil")

						sqlKasaYetkileri  = get_object_or_404(KasaYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						kasaYetkileriList = []
						if(sqlKasaYetkileri.IsKasaOlustur == True):
							kasaYetkileriList.append("Kasa Oluştur")
						if(sqlKasaYetkileri.IsKasaListele == True):
							kasaYetkileriList.append("Kasa Listele")
						if(sqlKasaYetkileri.IsKasaDetay == True):
							kasaYetkileriList.append("Kasa Detay")
						if(sqlKasaYetkileri.IsKasaGuncelle == True):
							kasaYetkileriList.append("Kasa Güncelle")
						if(sqlKasaYetkileri.IsKasaSil == True):
							kasaYetkileriList.append("Kasa Sil")

						sqlKasaHareketleriYetkileri  = get_object_or_404(KasaHareketleriYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						kasaHareketleriYetkileriList = []
						if(sqlKasaHareketleriYetkileri.IsKasaHareketleriOlustur == True):
							kasaHareketleriYetkileriList.append("Kasa Hareketleri Oluştur")
						if(sqlKasaHareketleriYetkileri.IsKasaHareketleriListele == True):
							kasaHareketleriYetkileriList.append("Kasa Hareketleri Listele")
						if(sqlKasaHareketleriYetkileri.IsKasaHareketleriDetay == True):
							kasaHareketleriYetkileriList.append("Kasa Hareketleri Detay")
						if(sqlKasaHareketleriYetkileri.IsKasaHareketleriIptalEt == True):
							kasaHareketleriYetkileriList.append("Kasa Hareketleri İptal Et")
						if(sqlKasaHareketleriYetkileri.IsKasaHareketleriSil == True):
							kasaHareketleriYetkileriList.append("Kasa Hareketleri Sil")

						sqlBankaYetkileri  = get_object_or_404(BankaYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						bankaYetkileriList = []
						if(sqlBankaYetkileri.IsBankaOlustur == True):
							bankaYetkileriList.append("Banka Oluştur")
						if(sqlBankaYetkileri.IsBankaListele == True):
							bankaYetkileriList.append("Banka Listele")
						if(sqlBankaYetkileri.IsBankaDetay == True):
							bankaYetkileriList.append("Banka Detay")
						if(sqlBankaYetkileri.IsBankaGuncelle == True):
							bankaYetkileriList.append("Banka Güncelle")
						if(sqlBankaYetkileri.IsBankaSil == True):
							bankaYetkileriList.append("Banka Sil")

						sqlBankaHareketleriYetkileri  = get_object_or_404(BankaHareketleriYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						bankaHareketleriYetkileriList = []
						if(sqlBankaHareketleriYetkileri.IsBankaHareketleriOlustur == True):
							bankaHareketleriYetkileriList.append("Banka Hareketleri Oluştur")
						if(sqlBankaHareketleriYetkileri.IsBankaHareketleriListele == True):
							bankaHareketleriYetkileriList.append("Banka Hareketleri Listele")
						if(sqlBankaHareketleriYetkileri.IsBankaHareketleriDetay == True):
							bankaHareketleriYetkileriList.append("Banka Hareketleri Detay")
						if(sqlBankaHareketleriYetkileri.IsBankaHareketleriIptalEt == True):
							bankaHareketleriYetkileriList.append("Banka Hareketleri İptal Et")
						if(sqlBankaHareketleriYetkileri.IsBankaHareketleriSil == True):
							bankaHareketleriYetkileriList.append("Banka Hareketleri Sil")

						sqlCariYetkileri  = get_object_or_404(CariYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						cariYetkileriList = []
						if(sqlCariYetkileri.IsCariOlustur == True):
							cariYetkileriList.append("Cari Oluştur")
						if(sqlCariYetkileri.IsCariListele == True):
							cariYetkileriList.append("Cari Listele")
						if(sqlCariYetkileri.IsCariDetay == True):
							cariYetkileriList.append("Cari Detay")
						if(sqlCariYetkileri.IsCariGuncelle == True):
							cariYetkileriList.append("Cari Güncelle")
						if(sqlCariYetkileri.IsCariSil == True):
							cariYetkileriList.append("Cari Sil")

						sqlCariHareketleriYetkileri  = get_object_or_404(CariHareketleriYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						cariHareketleriYetkileriList = []
						if(sqlCariHareketleriYetkileri.IsCariHareketleriListele == True):
							cariHareketleriYetkileriList.append("Cari Hareketleri Listele")
						if(sqlCariHareketleriYetkileri.IsCariHareketleriDetay == True):
							cariHareketleriYetkileriList.append("Cari Hareketleri Detay")

						sqlCekSenetYetkileri  = get_object_or_404(CekSenetYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						cekSenetYetkileriList = []
						if(sqlCekSenetYetkileri.IsCekBordroOlustur == True):
							cekSenetYetkileriList.append("Çek Bordro Oluştur")	
						if(sqlCekSenetYetkileri.IsCekListele == True):
							cekSenetYetkileriList.append("Çek Listele")
						if(sqlCekSenetYetkileri.IsCekDetay == True):
							cekSenetYetkileriList.append("Çek Detay")
						if(sqlCekSenetYetkileri.IsCekIptalEt == True):
							cekSenetYetkileriList.append("Çek İptal Et")
						if(sqlCekSenetYetkileri.IsCekIslemler == True):
							cekSenetYetkileriList.append("Çek İşlemler")	
						if(sqlCekSenetYetkileri.IsCekSil == True):
							cekSenetYetkileriList.append("Çek Sil")
						if(sqlCekSenetYetkileri.IsSenetBordroOlustur == True):
							cekSenetYetkileriList.append("Senet Bordro Oluştur")	
						if(sqlCekSenetYetkileri.IsSenetListele == True):
							cekSenetYetkileriList.append("Senet Listele")
						if(sqlCekSenetYetkileri.IsSenetDetay == True):
							cekSenetYetkileriList.append("Senet Detay")
						if(sqlCekSenetYetkileri.IsSenetIptalEt == True):
							cekSenetYetkileriList.append("Senet İptal Et")	
						if(sqlCekSenetYetkileri.IsSenetIslemler == True):
							cekSenetYetkileriList.append("Senet İşlemler")
						if(sqlCekSenetYetkileri.IsSenetSil == True):
							cekSenetYetkileriList.append("Senet Sil")		


						sqlFaturaYetkileri  = get_object_or_404(FaturaYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						faturaYetkileriList = []
						if(sqlFaturaYetkileri.IsFaturaOlustur == True):
							faturaYetkileriList.append("Fatura Oluştur")
						if(sqlFaturaYetkileri.IsFaturaListele == True):
							faturaYetkileriList.append("Fatura Listele")
						if(sqlFaturaYetkileri.IsFaturaDetay == True):
							faturaYetkileriList.append("Fatura Detay")
						if(sqlFaturaYetkileri.IsFaturaIptalEt == True):
							faturaYetkileriList.append("Fatura İptal Et")
						if(sqlFaturaYetkileri.IsFaturaIrsaliye == True):
							faturaYetkileriList.append("Fatura İrsaliye")	
						if(sqlFaturaYetkileri.IsFaturaSil == True):
							faturaYetkileriList.append("Fatura Sil")

						sqlIrsaliyeYetkileri  = get_object_or_404(IrsaliyeYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						irsaliyeYetkileriList = []
						if(sqlIrsaliyeYetkileri.IsIrsaliyeOlustur == True):
							irsaliyeYetkileriList.append("İrsaliye Oluştur")
						if(sqlIrsaliyeYetkileri.IsIrsaliyeListele == True):
							irsaliyeYetkileriList.append("İrsaliye Listele")
						if(sqlIrsaliyeYetkileri.IsIrsaliyeDetay == True):
							irsaliyeYetkileriList.append("İrsaliye Detay")
						if(sqlIrsaliyeYetkileri.IsIrsaliyeIptalEt == True):
							irsaliyeYetkileriList.append("İrsaliye İptal Et")
						if(sqlIrsaliyeYetkileri.IsIrsaliyeFatura == True):
							irsaliyeYetkileriList.append("İrsaliye Fatura")	
						if(sqlIrsaliyeYetkileri.IsIrsaliyeSil == True):
							irsaliyeYetkileriList.append("İrsaliye Sil")


						sqlSiparisYetkileri  = get_object_or_404(SiparisYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						siparisYetkileriList = []
						if(sqlSiparisYetkileri.IsSiparisOlustur == True):
							siparisYetkileriList.append("Sipariş Oluştur")
						if(sqlSiparisYetkileri.IsSiparisListele == True):
							siparisYetkileriList.append("Sipariş Listele")
						if(sqlSiparisYetkileri.IsSiparisDetay == True):
							siparisYetkileriList.append("Sipariş Detay")
						if(sqlSiparisYetkileri.IsSiparisIptalEt == True):
							siparisYetkileriList.append("Sipariş İptal Et")
						if(sqlSiparisYetkileri.IsSiparisFatura == True):
							siparisYetkileriList.append("Sipariş Fatura")	
						if(sqlSiparisYetkileri.IsSiparisSil == True):
							siparisYetkileriList.append("Sipariş Sil")


						sqlStokYetkileri  = get_object_or_404(StokYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						stokYetkileriList = []
						if(sqlStokYetkileri.IsStokOlustur == True):
							stokYetkileriList.append("Stok Oluştur")
						if(sqlStokYetkileri.IsStokListele == True):
							stokYetkileriList.append("Stok Listele")
						if(sqlStokYetkileri.IsStokDetay == True):
							stokYetkileriList.append("Stok Detay")
						if(sqlStokYetkileri.IsStokGuncelle == True):
							stokYetkileriList.append("Stok Güncelle")
						if(sqlStokYetkileri.IsStokSil == True):
							stokYetkileriList.append("Stok Sil")

						sqlStokHareketleriYetkileri  = get_object_or_404(StokHareketleriYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						stokHareketleriYetkileriList = []
						if(sqlStokHareketleriYetkileri.IsStokHareketleriListele == True):
							stokHareketleriYetkileriList.append("Stok Hareketleri Listele")
						if(sqlStokHareketleriYetkileri.IsStokHareketleriDetay == True):
							stokHareketleriYetkileriList.append("Stok Hareketleri Detay")
						

						sqlTanimlamaYetkileri  = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=ajaxKullaniciTipleri)
						tanimlamaYetkileriList = []
						if(sqlTanimlamaYetkileri.IsAnasayfaTanimlamalari == True):
							tanimlamaYetkileriList.append("Anasayfa Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsKasaTanimlamalari == True):
							tanimlamaYetkileriList.append("Kasa Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsBankaTanimlamalari == True):
							tanimlamaYetkileriList.append("Banka Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsCekSenetTanimlamalari == True):
							tanimlamaYetkileriList.append("Çek-Senet Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsSiparisTanimlamalari == True):
							tanimlamaYetkileriList.append("Sipariş Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsFaturaTanimlamalari == True):
							tanimlamaYetkileriList.append("Fatura Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsIrsaliyeTanimlamalari == True):
							tanimlamaYetkileriList.append("İrsaliye Tanımlamaları")
						if(sqlTanimlamaYetkileri.IsKullaniciTanimlamalari == True):
							tanimlamaYetkileriList.append("Kullanıcı Tanımlamaları")		

						context = {
							"ajaxModulYetkileri"            : modulYetkileriList,
							"ajaxKullanicilarYetkileri"     : kullaniciYetkileriList,
							"ajaxKasaYetkileri"             : kasaYetkileriList,
							"ajaxKasaHareketleriYetkileri"  : kasaHareketleriYetkileriList,
							"ajaxBankaYetkileri"            : bankaYetkileriList,
							"ajaxBankaHareketleriYetkileri" : bankaHareketleriYetkileriList,
							"ajaxCariYetkileri" 			: cariYetkileriList,
							"ajaxCariHareketleriYetkileri"	: cariHareketleriYetkileriList,
							"ajaxCekSenetYetkileri" 		: cekSenetYetkileriList,
							"ajaxFaturaYetkileri" 			: faturaYetkileriList,
							"ajaxIrsaliyeYetkileri"			: irsaliyeYetkileriList,
							"ajaxSiparisYetkileri"			: siparisYetkileriList,
							"ajaxStokYetkileri"				: stokYetkileriList,
							"ajaxStokHareketleriYetkileri"  : stokHareketleriYetkileriList,
							"ajaxTanimlamaYetkileri"        : tanimlamaYetkileriList,
						}
						return JsonResponse(context)

					ajaxKullaniciTipiKodu  = request.POST.get("ajaxKullaniciTipiKodu")
					ajaxKullaniciTipi      = request.POST.get("ajaxKullaniciTipi")
					
					ajaxIsAnaSayfa     = request.POST.get("ajaxIsAnaSayfa")
					ajaxIsCari 	       = request.POST.get("ajaxIsCari")
					ajaxIsKasa         = request.POST.get("ajaxIsKasa")
					ajaxIsBanka 	   = request.POST.get("ajaxIsBanka")
					ajaxIsCekSenet     = request.POST.get("ajaxIsCekSenet")
					ajaxIsSiparis 	   = request.POST.get("ajaxIsSiparis")
					ajaxIsFatura 	   = request.POST.get("ajaxIsFatura")
					ajaxIsIrsaliye 	   = request.POST.get("ajaxIsIrsaliye")
					ajaxIsStok 		   = request.POST.get("ajaxIsStok")			
					ajaxIsKullanicilar = request.POST.get("ajaxIsKullanicilar")
					ajaxIsTanimlamalar = request.POST.get("ajaxIsTanimlamalar")

					ajaxIsKullaniciOlustur  = request.POST.get("ajaxIsKullaniciOlustur")
					ajaxIsKullaniciListele  = request.POST.get("ajaxIsKullaniciListele")
					ajaxIsKullaniciDetay    = request.POST.get("ajaxIsKullaniciDetay")
					ajaxIsKullaniciGuncelle = request.POST.get("ajaxIsKullaniciGuncelle")			
					ajaxIsKullaniciSil	    = request.POST.get("ajaxIsKullaniciSil")

					ajaxIsCariOlustur  = request.POST.get("ajaxIsCariOlustur")
					ajaxIsCariListele  = request.POST.get("ajaxIsCariListele")
					ajaxIsCariDetay    = request.POST.get("ajaxIsCariDetay")
					ajaxIsCariGuncelle = request.POST.get("ajaxIsCariGuncelle")			
					ajaxIsCariSil	   = request.POST.get("ajaxIsCariSil")

					ajaxIsCariHareketleriListele = request.POST.get("ajaxIsCariHareketleriListele")
					ajaxIsCariHareketleriDetay   = request.POST.get("ajaxIsCariHareketleriDetay")

					ajaxIsKasaOlustur  = request.POST.get("ajaxIsKasaOlustur")
					ajaxIsKasaListele  = request.POST.get("ajaxIsKasaListele")
					ajaxIsKasaDetay    = request.POST.get("ajaxIsKasaDetay")
					ajaxIsKasaGuncelle = request.POST.get("ajaxIsKasaGuncelle")			
					ajaxIsKasaSil	   = request.POST.get("ajaxIsKasaSil")

					ajaxIsKasaHareketleriOlustur  = request.POST.get("ajaxIsKasaHareketleriOlustur")
					ajaxIsKasaHareketleriListele  = request.POST.get("ajaxIsKasaHareketleriListele")
					ajaxIsKasaHareketleriDetay    = request.POST.get("ajaxIsKasaHareketleriDetay")
					ajaxIsKasaHareketleriIptalEt  = request.POST.get("ajaxIsKasaHareketleriIptalEt")			
					ajaxIsKasaHareketleriSil	  = request.POST.get("ajaxIsKasaHareketleriSil")

					ajaxIsBankaOlustur  = request.POST.get("ajaxIsBankaOlustur")
					ajaxIsBankaListele  = request.POST.get("ajaxIsBankaListele")
					ajaxIsBankaDetay    = request.POST.get("ajaxIsBankaDetay")
					ajaxIsBankaGuncelle = request.POST.get("ajaxIsBankaGuncelle")			
					ajaxIsBankaSil	    = request.POST.get("ajaxIsBankaSil")

					ajaxIsBankaHareketleriOlustur = request.POST.get("ajaxIsBankaHareketleriOlustur")
					ajaxIsBankaHareketleriListele = request.POST.get("ajaxIsBankaHareketleriListele")
					ajaxIsBankaHareketleriDetay   = request.POST.get("ajaxIsBankaHareketleriDetay")
					ajaxIsBankaHareketleriIptalEt = request.POST.get("ajaxIsBankaHareketleriIptalEt")			
					ajaxIsBankaHareketleriSil	  = request.POST.get("ajaxIsBankaHareketleriSil")

					ajaxIsCekBordroOlustur   = request.POST.get("ajaxIsCekBordroOlustur")
					ajaxIsCekListele         = request.POST.get("ajaxIsCekListele")
					ajaxIsCekDetay           = request.POST.get("ajaxIsCekDetay")
					ajaxIsCekIslemler        = request.POST.get("ajaxIsCekIslemler")
					ajaxIsCekIptalEt         = request.POST.get("ajaxIsCekIptalEt")			
					ajaxIsCekSil             = request.POST.get("ajaxIsCekSil")
					ajaxIsSenetBordroOlustur = request.POST.get("ajaxIsSenetBordroOlustur")
					ajaxIsSenetListele       = request.POST.get("ajaxIsSenetListele")
					ajaxIsSenetDetay         = request.POST.get("ajaxIsSenetDetay")
					ajaxIsSenetIslemler      = request.POST.get("ajaxIsSenetIslemler")
					ajaxIsSenetIptalEt       = request.POST.get("ajaxIsSenetIptalEt")			
					ajaxIsSenetSil           = request.POST.get("ajaxIsSenetSil")

					ajaxIsCeklerListele   = request.POST.get("ajaxIsCeklerListele")
					ajaxIsCeklerDetay     = request.POST.get("ajaxIsCeklerDetay")
					ajaxIsSenetlerListele = request.POST.get("ajaxIsSenetlerListele")
					ajaxIsSenetlerDetay   = request.POST.get("ajaxIsSenetlerDetay")

					ajaxIsSiparisOlustur = request.POST.get("ajaxIsSiparisOlustur")
					ajaxIsSiparisListele = request.POST.get("ajaxIsSiparisListele")
					ajaxIsSiparisDetay   = request.POST.get("ajaxIsSiparisDetay")
					ajaxIsSiparisIptalEt = request.POST.get("ajaxIsSiparisIptalEt")
					ajaxIsSiparisFatura  = request.POST.get("ajaxIsSiparisFatura")
					ajaxIsSiparisSil     = request.POST.get("ajaxIsSiparisSil")

					ajaxIsFaturaOlustur  = request.POST.get("ajaxIsFaturaOlustur")
					ajaxIsFaturaListele  = request.POST.get("ajaxIsFaturaListele")
					ajaxIsFaturaDetay    = request.POST.get("ajaxIsFaturaDetay")
					ajaxIsFaturaIptalEt  = request.POST.get("ajaxIsFaturaIptalEt")
					ajaxIsFaturaIrsaliye = request.POST.get("ajaxIsFaturaIrsaliye")			
					ajaxIsFaturaSil      = request.POST.get("ajaxIsFaturaSil")

					ajaxIsIrsaliyeOlustur = request.POST.get("ajaxIsIrsaliyeOlustur")
					ajaxIsIrsaliyeListele = request.POST.get("ajaxIsIrsaliyeListele")
					ajaxIsIrsaliyeDetay   = request.POST.get("ajaxIsIrsaliyeDetay")
					ajaxIsIrsaliyeIptalEt = request.POST.get("ajaxIsIrsaliyeIptalEt")
					ajaxIsIrsaliyeFatura  = request.POST.get("ajaxIsIrsaliyeFatura")
					ajaxIsIrsaliyeSil     = request.POST.get("ajaxIsIrsaliyeSil")

					ajaxIsStokOlustur  = request.POST.get("ajaxIsStokOlustur")
					ajaxIsStokListele  = request.POST.get("ajaxIsStokListele")
					ajaxIsStokDetay    = request.POST.get("ajaxIsStokDetay")
					ajaxIsStokGuncelle = request.POST.get("ajaxIsStokGuncelle")			
					ajaxIsStokSil	   = request.POST.get("ajaxIsStokSil")

					ajaxIsStokHareketleriListele  = request.POST.get("ajaxIsStokHareketleriListele")
					ajaxIsStokHareketleriDetay    = request.POST.get("ajaxIsStokHareketleriDetay")

					ajaxIsAnasayfaTanimlamalari  = request.POST.get("ajaxIsAnasayfaTanimlamalari")
					ajaxIsKasaTanimlamalari  = request.POST.get("ajaxIsKasaTanimlamalari")
					ajaxIsBankaTanimlamalari    = request.POST.get("ajaxIsBankaTanimlamalari")
					ajaxIsCekSenetTanimlamalari = request.POST.get("ajaxIsCekSenetTanimlamalari")			
					ajaxIsSiparisTanimlamalari	   = request.POST.get("ajaxIsSiparisTanimlamalari")
					ajaxIsFaturaTanimlamalari  = request.POST.get("ajaxIsFaturaTanimlamalari")
					ajaxIsIrsaliyeTanimlamalari  = request.POST.get("ajaxIsIrsaliyeTanimlamalari")
					ajaxIsKullaniciTanimlamalari    = request.POST.get("ajaxIsKullaniciTanimlamalari")

					if(ajaxKullaniciTipi):
						sqlKullaniciTanimlamalari = KullaniciTipiModel()
						sqlKullaniciTanimlamalari.KullaniciTipiKodu = ajaxKullaniciTipiKodu
						sqlKullaniciTanimlamalari.KullaniciTipi     = ajaxKullaniciTipi
						sqlKullaniciTanimlamalari.save()

						sqlModulYetkileri =  ModulYetkileri()
						sqlModulYetkileri.KullaniciTipiKodu  = ajaxKullaniciTipiKodu
						sqlModulYetkileri.IsAnaSayfa         = ajaxIsAnaSayfa
						sqlModulYetkileri.IsCari 		     = ajaxIsCari
						sqlModulYetkileri.IsKasa 		     = ajaxIsKasa
						sqlModulYetkileri.IsBanka 		     = ajaxIsBanka
						sqlModulYetkileri.IsCekSenet 	     = ajaxIsCekSenet
						sqlModulYetkileri.IsSiparis          = ajaxIsSiparis
						sqlModulYetkileri.IsFatura 	         = ajaxIsFatura
						sqlModulYetkileri.IsIrsaliye         = ajaxIsIrsaliye
						sqlModulYetkileri.IsStok 		     = ajaxIsStok
						sqlModulYetkileri.IsKullanicilar     = ajaxIsKullanicilar
						sqlModulYetkileri.IsTanimlamalar     = ajaxIsTanimlamalar		
						sqlModulYetkileri.save()

						sqlKullanicilarYetkileri = KullaniciYetkileri()
						sqlKullanicilarYetkileri.KullaniciTipiKodu   = ajaxKullaniciTipiKodu
						sqlKullanicilarYetkileri.IsKullaniciOlustur  = ajaxIsKullaniciOlustur
						sqlKullanicilarYetkileri.IsKullaniciListele  = ajaxIsKullaniciListele
						sqlKullanicilarYetkileri.IsKullaniciDetay    = ajaxIsKullaniciDetay
						sqlKullanicilarYetkileri.IsKullaniciGuncelle = ajaxIsKullaniciGuncelle
						sqlKullanicilarYetkileri.IsKullaniciSil      = ajaxIsKullaniciSil
						sqlKullanicilarYetkileri.save()

						sqlCariYetkileri = CariYetkileri()
						sqlCariYetkileri.KullaniciTipiKodu  = ajaxKullaniciTipiKodu
						sqlCariYetkileri.IsCariOlustur      = ajaxIsCariOlustur
						sqlCariYetkileri.IsCariListele      = ajaxIsCariListele
						sqlCariYetkileri.IsCariDetay        = ajaxIsCariDetay
						sqlCariYetkileri.IsCariGuncelle     = ajaxIsCariGuncelle
						sqlCariYetkileri.IsCariSil          = ajaxIsCariSil
						sqlCariYetkileri.save()

						sqlCariHareketleriYetkileri = CariHareketleriYetkileri()
						sqlCariHareketleriYetkileri.KullaniciTipiKodu         = ajaxKullaniciTipiKodu
						sqlCariHareketleriYetkileri.IsCariHareketleriListele  = ajaxIsCariHareketleriListele
						sqlCariHareketleriYetkileri.IsCariHareketleriDetay    = ajaxIsCariHareketleriDetay
						sqlCariHareketleriYetkileri.save()

						sqlKasaYetkileri = KasaYetkileri()
						sqlKasaYetkileri.KullaniciTipiKodu 	 = ajaxKullaniciTipiKodu
						sqlKasaYetkileri.IsKasaOlustur       = ajaxIsKasaOlustur
						sqlKasaYetkileri.IsKasaListele       = ajaxIsKasaListele
						sqlKasaYetkileri.IsKasaDetay         = ajaxIsKasaDetay
						sqlKasaYetkileri.IsKasaGuncelle      = ajaxIsKasaGuncelle
						sqlKasaYetkileri.IsKasaSil           = ajaxIsKasaSil
						sqlKasaYetkileri.save()

						sqlKasaHareketleriYetkileri = KasaHareketleriYetkileri()
						sqlKasaHareketleriYetkileri.KullaniciTipiKodu 		 = ajaxKullaniciTipiKodu
						sqlKasaHareketleriYetkileri.IsKasaHareketleriOlustur = ajaxIsKasaHareketleriOlustur
						sqlKasaHareketleriYetkileri.IsKasaHareketleriListele = ajaxIsKasaHareketleriListele
						sqlKasaHareketleriYetkileri.IsKasaHareketleriDetay   = ajaxIsKasaHareketleriDetay
						sqlKasaHareketleriYetkileri.IsKasaHareketleriIptalEt = ajaxIsKasaHareketleriIptalEt
						sqlKasaHareketleriYetkileri.IsKasaHareketleriSil     = ajaxIsKasaHareketleriSil
						sqlKasaHareketleriYetkileri.save()

						sqlBankaYetkileri = BankaYetkileri()
						sqlBankaYetkileri.KullaniciTipiKodu   = ajaxKullaniciTipiKodu
						sqlBankaYetkileri.IsBankaOlustur      = ajaxIsBankaOlustur
						sqlBankaYetkileri.IsBankaListele      = ajaxIsBankaListele
						sqlBankaYetkileri.IsBankaDetay        = ajaxIsBankaDetay
						sqlBankaYetkileri.IsBankaGuncelle     = ajaxIsBankaGuncelle
						sqlBankaYetkileri.IsBankaSil          = ajaxIsBankaSil
						sqlBankaYetkileri.save()

						sqlBankaHareketleriYetkileri = BankaHareketleriYetkileri()
						sqlBankaHareketleriYetkileri.KullaniciTipiKodu 		   = ajaxKullaniciTipiKodu
						sqlBankaHareketleriYetkileri.IsBankaHareketleriOlustur = ajaxIsBankaHareketleriOlustur
						sqlBankaHareketleriYetkileri.IsBankaHareketleriListele = ajaxIsBankaHareketleriListele
						sqlBankaHareketleriYetkileri.IsBankaHareketleriDetay   = ajaxIsBankaHareketleriDetay
						sqlBankaHareketleriYetkileri.IsBankaHareketleriIptalEt = ajaxIsBankaHareketleriIptalEt
						sqlBankaHareketleriYetkileri.IsBankaHareketleriSil     = ajaxIsBankaHareketleriSil
						sqlBankaHareketleriYetkileri.save()

						sqlCekSenetYetkileri = CekSenetYetkileri()
						sqlCekSenetYetkileri.KullaniciTipiKodu    = ajaxKullaniciTipiKodu
						sqlCekSenetYetkileri.IsCekBordroOlustur   = ajaxIsCekBordroOlustur
						sqlCekSenetYetkileri.IsCekListele         = ajaxIsCekListele
						sqlCekSenetYetkileri.IsCekDetay           = ajaxIsCekDetay
						sqlCekSenetYetkileri.IsCekIslemler        = ajaxIsCekIslemler
						sqlCekSenetYetkileri.IsCekIptalEt         = ajaxIsCekIptalEt
						sqlCekSenetYetkileri.IsCekSil             = ajaxIsCekSil
						sqlCekSenetYetkileri.IsSenetBordroOlustur = ajaxIsSenetBordroOlustur
						sqlCekSenetYetkileri.IsSenetListele       = ajaxIsSenetListele
						sqlCekSenetYetkileri.IsSenetDetay         = ajaxIsSenetDetay
						sqlCekSenetYetkileri.IsSenetIslemler      = ajaxIsSenetIslemler
						sqlCekSenetYetkileri.IsSenetIptalEt       = ajaxIsSenetIptalEt
						sqlCekSenetYetkileri.IsSenetSil           = ajaxIsSenetSil
						sqlCekSenetYetkileri.save()

						sqlSiparisYetkileri = SiparisYetkileri()
						sqlSiparisYetkileri.KullaniciTipiKodu = ajaxKullaniciTipiKodu
						sqlSiparisYetkileri.IsSiparisOlustur  = ajaxIsSiparisOlustur
						sqlSiparisYetkileri.IsSiparisListele  = ajaxIsSiparisListele
						sqlSiparisYetkileri.IsSiparisDetay    = ajaxIsSiparisDetay
						sqlSiparisYetkileri.IsSiparisIptalEt  = ajaxIsSiparisIptalEt
						sqlSiparisYetkileri.IsSiparisFatura   = ajaxIsSiparisFatura
						sqlSiparisYetkileri.IsSiparisSil      = ajaxIsSiparisSil
						sqlSiparisYetkileri.save()

						sqlFaturaYetkileri = FaturaYetkileri()
						sqlFaturaYetkileri.KullaniciTipiKodu = ajaxKullaniciTipiKodu
						sqlFaturaYetkileri.IsFaturaOlustur   = ajaxIsFaturaOlustur
						sqlFaturaYetkileri.IsFaturaListele   = ajaxIsFaturaListele
						sqlFaturaYetkileri.IsFaturaDetay     = ajaxIsFaturaDetay
						sqlFaturaYetkileri.IsFaturaIptalEt   = ajaxIsFaturaIptalEt
						sqlFaturaYetkileri.IsFaturaIrsaliye  = ajaxIsFaturaIrsaliye
						sqlFaturaYetkileri.IsFaturaSil       = ajaxIsFaturaSil
						sqlFaturaYetkileri.save()

						sqlIrsaliyeYetkileri = IrsaliyeYetkileri()
						sqlIrsaliyeYetkileri.KullaniciTipiKodu = ajaxKullaniciTipiKodu
						sqlIrsaliyeYetkileri.IsIrsaliyeOlustur = ajaxIsIrsaliyeOlustur
						sqlIrsaliyeYetkileri.IsIrsaliyeListele = ajaxIsIrsaliyeListele
						sqlIrsaliyeYetkileri.IsIrsaliyeDetay   = ajaxIsIrsaliyeDetay
						sqlIrsaliyeYetkileri.IsIrsaliyeIptalEt = ajaxIsIrsaliyeIptalEt
						sqlIrsaliyeYetkileri.IsIrsaliyeFatura  = ajaxIsIrsaliyeFatura
						sqlIrsaliyeYetkileri.IsIrsaliyeSil     = ajaxIsIrsaliyeSil
						sqlIrsaliyeYetkileri.save()

						sqlStokYetkileri = StokYetkileri()
						sqlStokYetkileri.KullaniciTipiKodu = ajaxKullaniciTipiKodu
						sqlStokYetkileri.IsStokOlustur     = ajaxIsStokOlustur
						sqlStokYetkileri.IsStokListele     = ajaxIsStokListele
						sqlStokYetkileri.IsStokDetay       = ajaxIsStokDetay
						sqlStokYetkileri.IsStokGuncelle    = ajaxIsStokGuncelle
						sqlStokYetkileri.IsStokSil         = ajaxIsStokSil
						sqlStokYetkileri.save()

						sqlStokHareketleriYetkileri = StokHareketleriYetkileri()
						sqlStokHareketleriYetkileri.KullaniciTipiKodu 		 = ajaxKullaniciTipiKodu
						sqlStokHareketleriYetkileri.IsStokHareketleriListele = ajaxIsStokHareketleriListele
						sqlStokHareketleriYetkileri.IsStokHareketleriDetay   = ajaxIsStokHareketleriDetay
						sqlStokHareketleriYetkileri.save()

						sqlTanimlamaYetkileri = TanimlamaYetkileri()
						sqlTanimlamaYetkileri.KullaniciTipiKodu        = ajaxKullaniciTipiKodu
						sqlTanimlamaYetkileri.IsAnasayfaTanimlamalari  = ajaxIsAnasayfaTanimlamalari
						sqlTanimlamaYetkileri.IsKasaTanimlamalari      = ajaxIsKasaTanimlamalari
						sqlTanimlamaYetkileri.IsBankaTanimlamalari     = ajaxIsBankaTanimlamalari
						sqlTanimlamaYetkileri.IsCekSenetTanimlamalari  = ajaxIsCekSenetTanimlamalari
						sqlTanimlamaYetkileri.IsSiparisTanimlamalari   = ajaxIsSiparisTanimlamalari
						sqlTanimlamaYetkileri.IsFaturaTanimlamalari    = ajaxIsFaturaTanimlamalari
						sqlTanimlamaYetkileri.IsIrsaliyeTanimlamalari  = ajaxIsIrsaliyeTanimlamalari
						sqlTanimlamaYetkileri.IsKullaniciTanimlamalari = ajaxIsKullaniciTanimlamalari
						sqlTanimlamaYetkileri.save()

						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)
					
				varKullaniciTipiModel = KullaniciTipiModel.objects.all()
				varKullaniciGrubuModel = KullaniciGrubuModel.objects.all()
				
				context = {
					"modulYetkisi"           : modulYetkisi,
					"varKullaniciTipiModel"  : varKullaniciTipiModel,
					"varKullaniciGrubuModel" : varKullaniciGrubuModel,
				}		
				return render (request, "kullanicilar/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")