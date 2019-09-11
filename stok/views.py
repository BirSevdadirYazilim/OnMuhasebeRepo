from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

suan = timezone.now()

def StokOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsStok == True):
			islemlerKontrol = get_object_or_404(StokYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsStokOlustur == True):
				if request.is_ajax():
					ajaxStokKodu 	   = request.POST.get("ajaxStokKodu")
					ajaxStokAdi 	   = request.POST.get("ajaxStokAdi")
					ajaxStokNitelik    = request.POST.get("ajaxStokNitelik")
					ajaxStokMiktar     = request.POST.get("ajaxStokMiktar")
					ajaxAlisFiyati     = request.POST.get("ajaxAlisFiyati")
					ajaxSatisFiyati    = request.POST.get("ajaxSatisFiyati")
					ajaxKdvOrani 	   = request.POST.get("ajaxKdvOrani")
					ajaxKayitTarihi    = request.POST.get("ajaxKayitTarihi")
					alisFiyatiReplace  = ajaxAlisFiyati.replace(",",".")
					satisFiyatiReplace = ajaxSatisFiyati.replace(",",".")
					try:
						stokKoduKontrol = get_object_or_404(Stok,StokKodu=ajaxStokKodu)
						context = {"ajaxMesaj" : "Bu Stok Kodu Kullanılıyor !"}
						return JsonResponse(context)
					except:
						pass
					try:
						stokAdiKontrol = get_object_or_404(Stok,StokAdi=ajaxStokAdi)
						context = {"ajaxMesaj" : "Bu Stok Adı Kullanılıyor !"}
						return JsonResponse(context)
					except:
						pass		
					if(ajaxStokKodu and ajaxStokAdi and ajaxStokNitelik and ajaxStokMiktar and ajaxAlisFiyati and ajaxSatisFiyati and ajaxKdvOrani and ajaxKayitTarihi):
						sqlStok = Stok()
						sqlStok.StokKodu           = ajaxStokKodu
						sqlStok.StokAdi            = ajaxStokAdi
						sqlStok.StokNitelik        = ajaxStokNitelik
						sqlStok.StokMiktar         = ajaxStokMiktar
						sqlStok.AlisFiyati         = alisFiyatiReplace
						sqlStok.SatisFiyati        = satisFiyatiReplace
						sqlStok.KdvOrani 	       = ajaxKdvOrani
						sqlStok.StokKayitTarihi    = ajaxKayitTarihi
						sqlStok.StokKaydiOlusturan = request.session["KullaniciKodu"]
						sqlStok.save()

						sqlStokHareketleri = StokHareketleri()
						sqlStokHareketleri.StokKodu              = ajaxStokKodu
						sqlStokHareketleri.StokAdi               = ajaxStokAdi
						sqlStokHareketleri.StokNitelik           = ajaxStokNitelik
						sqlStokHareketleri.StokMiktar            = ajaxStokMiktar
						sqlStokHareketleri.AlisFiyati            = alisFiyatiReplace
						sqlStokHareketleri.SatisFiyati           = satisFiyatiReplace
						sqlStokHareketleri.KdvOrani 	         = ajaxKdvOrani
						sqlStokHareketleri.StokHareketTarihi     = ajaxKayitTarihi
						sqlStokHareketleri.StokHareketiOlusturan = request.session["KullaniciKodu"]
						sqlStokHareketleri.IsVerified 			 = True
						sqlStokHareketleri.save()
						context = {"ajaxMesaj": "1",}
						return JsonResponse(context)
					else:
						context = {"ajaxMesaj": "Lütfen Formu Boş Bırakmayınız !",}
						return JsonResponse(context)	
				context = {
					"modulYetkisi" : modulYetkisi,
					"suan"         : suan,
				}
				return render (request, "stok/olustur.html", context)		
			else:		
				messages.success(request, "Stok Oluşturma Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")				
	
def StokListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsStok == True):
			islemlerKontrol = get_object_or_404(StokYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsStokListele == True):
				if request.is_ajax():
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						sqlStok = get_object_or_404(Stok,id=ajaxSil)
						sqlStok.IsDeleted = True
						sqlStok.save()
						context = {"ajaxMesaj" : "Başarılı Bir Şekilde Silindi !",}
						return JsonResponse(context)

					ajaxDetay 	    = request.POST.get("ajaxDetay")	
					if(ajaxDetay):	
						sqlStok = get_object_or_404(Stok,id=ajaxDetay)
						context = {
							"ajaxStokKodu"            : sqlStok.StokKodu,
							"ajaxStokAdi"             : sqlStok.StokAdi,
							"ajaxStokNitelik"         : sqlStok.StokNitelik,
							"ajaxStokMiktar"          : sqlStok.StokMiktar,
							"ajaxAlisFiyati"          : sqlStok.AlisFiyati,
							"ajaxSatisFiyati"         : sqlStok.SatisFiyati,
							"ajaxKdvOrani"            : sqlStok.KdvOrani,
							"ajaxStokKaydiOlusturan"  : sqlStok.StokKaydiOlusturan,
							"ajaxStokKayitTarihi"     : sqlStok.StokKayitTarihi,
							"ajaxStokKaydiDuzenleyen" : sqlStok.StokKaydiDuzenleyen,
							"ajaxStokDuzenlemeTarihi" : sqlStok.StokDuzenlemeTarihi,
						}
						return JsonResponse(context)

					ajaxGuncelle 	    = request.POST.get("ajaxGuncelle")	
					if(ajaxGuncelle):	
						sqlStokGuncelle = get_object_or_404(Stok,id=ajaxGuncelle)
						context = {
							"ajaxStokIdGuncelle"       	  : sqlStokGuncelle.id,
							"ajaxStokKoduGuncelle"        : sqlStokGuncelle.StokKodu,
							"ajaxStokAdiGuncelle"         : sqlStokGuncelle.StokAdi,
							"ajaxStokNitelikGuncelle"     : sqlStokGuncelle.StokNitelik,
							"ajaxStokMiktarGuncelle"      : sqlStokGuncelle.StokMiktar,
							"ajaxAlisFiyatiGuncelle"      : sqlStokGuncelle.AlisFiyati,
							"ajaxSatisFiyatiGuncelle"     : sqlStokGuncelle.SatisFiyati,
							"ajaxKdvOraniGuncelle"        : sqlStokGuncelle.KdvOrani,
						}
						return JsonResponse(context)

					ajaxGuncelleKaydet 	   = request.POST.get("ajaxGuncelleKaydet")
					ajaxStokKodu		   = request.POST.get("ajaxStokKodu")
					ajaxStokAdi 	       = request.POST.get("ajaxStokAdi")
					ajaxStokNitelik 	   = request.POST.get("ajaxStokNitelik")
					ajaxStokMiktar         = request.POST.get("ajaxStokMiktar")
					ajaxAlisFiyati         = request.POST.get("ajaxAlisFiyati")
					ajaxSatisFiyati        = request.POST.get("ajaxSatisFiyati")
					ajaxKdvOrani 		   = request.POST.get("ajaxKdvOrani")
					ajaxAlisFiyatiReplace  = ajaxAlisFiyati.replace(",",".")
					ajaxSatisFiyatiReplace = ajaxSatisFiyati.replace(",",".")
					if(ajaxGuncelleKaydet):
						
						sqlStokGuncelleKaydet = get_object_or_404(Stok,id=ajaxGuncelleKaydet)
						sqlStokGuncelleKaydet.StokKodu 		      = ajaxStokKodu
						sqlStokGuncelleKaydet.StokAdi 		      = ajaxStokAdi
						sqlStokGuncelleKaydet.StokNitelik         = ajaxStokNitelik
						sqlStokGuncelleKaydet.StokMiktar          = ajaxStokMiktar
						sqlStokGuncelleKaydet.AlisFiyati          = ajaxAlisFiyatiReplace
						sqlStokGuncelleKaydet.SatisFiyati         = ajaxSatisFiyatiReplace
						sqlStokGuncelleKaydet.KdvOrani 		      = ajaxKdvOrani
						sqlStokGuncelleKaydet.StokKaydiDuzenleyen = request.session["KullaniciKodu"]
						sqlStokGuncelleKaydet.StokDuzenlemeTarihi = suan
						sqlStokGuncelleKaydet.save()
						context = {"ajaxMesajGuncelle" : "Başarılı Bir Şekilde Güncellendi !"}
						return JsonResponse(context)

				sqlListele = Stok.objects.filter(IsDeleted=False)
				context = {
					"modulYetkisi"    : modulYetkisi,
					"islemlerKontrol" : islemlerKontrol,
					"sqlListele"      : sqlListele,
				}
				return render (request, "stok/listele.html", context)		
			else:		
				messages.success(request, "Stok Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def StokHareketleriListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsStok == True):
			islemlerKontrol = get_object_or_404(StokHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsStokHareketleriListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlStok = get_object_or_404(StokHareketleri,id=ajaxDetay)
						if(sqlStok.AlisFiyati != None):
							varAlisFiyati = sqlStok.AlisFiyati
						else:
							varAlisFiyati = ""	
						if(sqlStok.SatisFiyati != None):
							varSatisFiyati = sqlStok.SatisFiyati
						else:
							varSatisFiyati = ""		
						context = {
							"ajaxStokKodu"           	: sqlStok.StokKodu,
							"ajaxStokAdi"            	: sqlStok.StokAdi,
							"ajaxStokNitelik"         	: sqlStok.StokNitelik,
							"ajaxStokMiktar"          	: sqlStok.StokMiktar,
							"ajaxAlisFiyati"          	: varAlisFiyati,
							"ajaxSatisFiyati"        	: varSatisFiyati,
							"ajaxSonIskontoOrani"     	: sqlStok.SonIskontoOrani,
							"ajaxStokHareketiOlusturan" : sqlStok.StokHareketiOlusturan,
							"ajaxStokHareketTarihi"     : sqlStok.StokHareketTarihi,
						}		
						return JsonResponse(context)
				sqlStokHareketleri = StokHareketleri.objects.all()
				context = {
					"modulYetkisi"       : modulYetkisi,
					"islemlerKontrol"    : islemlerKontrol,
					"sqlStokHareketleri" : sqlStokHareketleri,
				}
				return render (request, "stok/stokhareketleri.html", context)		
			else:		
				messages.success(request, "Stok Hareketleri Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")