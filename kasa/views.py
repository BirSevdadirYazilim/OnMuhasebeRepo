from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from banka.models import *
from cari.models import *
from fatura.models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

suan = timezone.now()

def KasaOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if (modulYetkisi.IsKasa == True):
			islemlerKontrol = get_object_or_404(KasaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKasaOlustur == True):
				if request.is_ajax():
					ajaxKasaKodu           = request.POST.get("ajaxKasaKodu")
					ajaxKasaAdi            = request.POST.get("ajaxKasaAdi")
					ajaxKasaAcilisBakiyesi = request.POST.get("ajaxKasaAcilisBakiyesi")
					ajaxKasaAcilisTarihi   = request.POST.get("ajaxKasaAcilisTarihi")
					ajaxAciklama           = request.POST.get("ajaxAciklama")
					if(ajaxKasaKodu != "" and ajaxKasaAdi != "" and ajaxKasaAcilisBakiyesi != "" and ajaxKasaAcilisTarihi != ""):
						try:
							# Kasa Kodu Mükerrer Kontrolu
							kasaKoduKontrol = get_object_or_404(Kasa,KasaKodu=ajaxKasaKodu)
							context = {"ajaxMesaj" : "Bu Kasa Kodu Kullanılıyor !"}
							return JsonResponse(context)
						except:
							pass
						try:
							# Kasa Adı Mükerrer Kontrolu
							kasaAdiKontrol = get_object_or_404(Kasa,KasaAdi=ajaxKasaAdi)
							context = {"ajaxMesaj" : "Bu Kasa Adı Kullanılıyor !"}
							return JsonResponse(context)
						except:
							pass		
						kasaOlustur = Kasa()
						kasaOlustur.KasaKodu           = ajaxKasaKodu
						kasaOlustur.KasaAdi            = ajaxKasaAdi
						kasaOlustur.KasaAcilisBakiyesi = ajaxKasaAcilisBakiyesi
						kasaOlustur.KasaBorc           = ajaxKasaAcilisBakiyesi
						kasaOlustur.KasaAlacak         = 0
						kasaOlustur.KasaKaydiOlusturan = request.session["KullaniciKodu"]
						kasaOlustur.KasaAcilisTarihi   = ajaxKasaAcilisTarihi
						kasaOlustur.Aciklama           = ajaxAciklama
						kasaOlustur.save()
						if(ajaxKasaAcilisBakiyesi == None):
							ajaxKasaAcilisBakiyesi = 0
							replaceKasaAcilisBakiyesi = 0
						else:
							replaceKasaAcilisBakiyesi = ajaxKasaAcilisBakiyesi.replace(",",".")	
						kasaHareketleriOlustur = KasaHareketleri()
						kasaHareketleriOlustur.KasaKodu      = ajaxKasaKodu
						kasaHareketleriOlustur.Makbuz        = "3"
						kasaHareketleriOlustur.MakbuzNo      = ""
						kasaHareketleriOlustur.MakbuzTarihi  = ajaxKasaAcilisTarihi
						kasaHareketleriOlustur.KasaBorc      = float(replaceKasaAcilisBakiyesi)
						kasaHareketleriOlustur.KasaAlacak    = 0
						kasaHareketleriOlustur.Aciklama      = ajaxAciklama
						kasaHareketleriOlustur.save()
						ajaxMesaj = "1"
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
					context = {"ajaxMesaj" : ajaxMesaj}
					return JsonResponse(context)
				context = {
					"modulYetkisi" : modulYetkisi,
					"suan"		   : suan,
				}
				return render (request, "kasa/olustur.html", context)
			else:		
				messages.success(request, "Kasa Kaydı Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")	
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")		

def KasaListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if (modulYetkisi.IsKasa == True):
			islemlerKontrol = get_object_or_404(KasaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKasaListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlKasaDetay = get_object_or_404(Kasa,id=ajaxDetay)
						context = {
							"ajaxKasaKodu"            : sqlKasaDetay.KasaKodu,
							"ajaxKasaAdi"             : sqlKasaDetay.KasaAdi,
							"ajaxKasaAcilisBakiyesi"  : sqlKasaDetay.KasaAcilisBakiyesi,
							"ajaxKasaAcilisTarihi"    : sqlKasaDetay.KasaAcilisTarihi,
							"ajaxKasaKaydiOlusturan"  : sqlKasaDetay.KasaKaydiOlusturan,
							"ajaxKasaBakiyesi"  	  : float(sqlKasaDetay.KasaBorc) - float(sqlKasaDetay.KasaAlacak),
							"ajaxKasaDuzenlemeTarihi" : sqlKasaDetay.KasaDuzenlemeTarihi,
							"ajaxKasaKaydıDuzenleyen" : sqlKasaDetay.KasaKaydıDuzenleyen,
							"ajaxAciklama"            : sqlKasaDetay.Aciklama,
						}
						return JsonResponse(context)
					ajaxGuncelle = request.POST.get("ajaxGuncelle")
					if(ajaxGuncelle):
						sqlKasaGuncelle = get_object_or_404(Kasa,id=ajaxGuncelle)
						context = {
							"ajaxIdGuncelle"       : sqlKasaGuncelle.id,
							"ajaxKasaKoduGuncelle" : sqlKasaGuncelle.KasaKodu,
							"ajaxKasaAdiGuncelle"  : sqlKasaGuncelle.KasaAdi,
							"ajaxAciklamaGuncelle" : sqlKasaGuncelle.Aciklama,
						}
						return JsonResponse(context)
					ajaxIdKaydet 	   = request.POST.get("ajaxIdKaydet")
					ajaxKasaAdiKaydet  = request.POST.get("ajaxKasaAdiKaydet")
					ajaxAciklamaKaydet = request.POST.get("ajaxAciklamaKaydet")
					if(ajaxIdKaydet):
						if(ajaxKasaAdiKaydet != ""):
							sqlKasaKaydet = get_object_or_404(Kasa,id=ajaxIdKaydet)
							sqlKasaKaydet.KasaAdi  = ajaxKasaAdiKaydet
							sqlKasaKaydet.Aciklama = ajaxAciklamaKaydet
							sqlKasaKaydet.save()
							ajaxMesaj = "1"
						else:
							ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
						context = {"ajaxMesaj" : ajaxMesaj,}
						return JsonResponse(context)
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						sqlKasaGuncelle = get_object_or_404(Kasa,id=ajaxSil)
						sqlKasaGuncelle.IsDeleted = True
						sqlKasaGuncelle.save()
						context = {"ajaxMesaj" : "Başarılı Bir Şekilde Silindi !",}
						return JsonResponse(context)	
				sqlKasa = Kasa.objects.filter(IsDeleted=False)
				bakiyeList = []
				for x in sqlKasa:
					bakiyeDemet = {"KasaId":x.id,"KasaKodu":x.KasaKodu,"KasaAdi":x.KasaAdi,\
					"KasaAcilisBakiyesi":x.KasaAcilisBakiyesi,"KasaBakiyesi":x.KasaBorc - x.KasaAlacak,\
					"KasaBorc":x.KasaBorc,"KasaAlacak":x.KasaAlacak}
					bakiyeList.append(bakiyeDemet)
				context = {
					"modulYetkisi"     : modulYetkisi,
					"islemlerKontrol"  : islemlerKontrol,
					"kullaniciKontrol" : modulYetkisi.IsBanka,
					"bakiyeList"       : bakiyeList,
				}
				return render (request, "kasa/listele.html", context)
			else:		
				messages.success(request, "Kasa Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")
		
def KasaHareketleriOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if (modulYetkisi.IsKasa == True):
			islemlerKontrol = get_object_or_404(KasaHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKasaHareketleriOlustur == True):
				if request.is_ajax():
					ajaxKasaMakbuzNoKontrol = request.POST.get("ajaxKasaMakbuzNoKontrol")
					ajaxMakbuzNoKontrol     = request.POST.get("ajaxMakbuzNoKontrol")
					if(ajaxKasaMakbuzNoKontrol and ajaxMakbuzNoKontrol):
						makbuzNo = None
						try:
							sqlMakbuzNo = get_object_or_404(MakbuzNo,KasaKodu=ajaxKasaMakbuzNoKontrol)
							if(ajaxMakbuzNoKontrol == "1"):
								if(sqlMakbuzNo.TahsilatMakbuzuNo != ""):
									makbuzNo = sqlMakbuzNo.TahsilatMakbuzuNo
								else:
									makbuzNo = None
							if(ajaxMakbuzNoKontrol == "2"):
								if(sqlMakbuzNo.TediyeMakbuzuNo != ""):
									makbuzNo = sqlMakbuzNo.TediyeMakbuzuNo
								else:
									makbuzNo = None
						except:
							makbuzNo = None
						context = {"ajaxSqlMakbuzNo" : makbuzNo,}
						return JsonResponse(context)

					ajaxBakiyeKontrol   = request.POST.get("ajaxBakiyeKontrol")
					ajaxKasaKoduKontrol = request.POST.get("ajaxKasaKoduKontrol")
					if(ajaxBakiyeKontrol):
						replaceBakiyeKontrol = ajaxBakiyeKontrol.replace(",",".")
						sqlKasaAdi = get_object_or_404(Kasa,KasaKodu=ajaxKasaKoduKontrol)
						if(float(sqlKasaAdi.KasaBorc - sqlKasaAdi.KasaAlacak) - float(replaceBakiyeKontrol) < 0):
							context = {"ajaxMesaj" : "Yetersiz Bakiye !"}
						else:
							context = {"ajaxMesaj" : ""}	
						return JsonResponse(context)	

					ajaxKasaKodu     = request.POST.get("ajaxKasaKodu")
					ajaxMakbuz       = request.POST.get("ajaxMakbuz")
					ajaxMakbuzNo     = request.POST.get("ajaxMakbuzNo")
					ajaxMakbuzTarihi = request.POST.get("ajaxMakbuzTarihi")
					ajaxTutar        = request.POST.get("ajaxTutar")
					ajaxAciklama     = request.POST.get("ajaxAciklama")
					ajaxCariUnvani   = request.POST.get("ajaxCariUnvani")
					if(ajaxKasaKodu != "" and ajaxMakbuz != "" and ajaxMakbuzNo != "" and ajaxMakbuzTarihi != "" and ajaxTutar != "" and ajaxCariUnvani != ""):
						replaceTutar = ajaxTutar.replace(",",".")	
						kasaHareketleriOlustur = KasaHareketleri()
						kasaHareketleriOlustur.KasaKodu     = ajaxKasaKodu
						kasaHareketleriOlustur.Makbuz       = ajaxMakbuz
						kasaHareketleriOlustur.MakbuzNo     = ajaxMakbuzNo
						kasaHareketleriOlustur.MakbuzTarihi = ajaxMakbuzTarihi
						if(ajaxMakbuz == "1"):
							kasaHareketleriOlustur.KasaBorc     = float(replaceTutar)
						if(ajaxMakbuz == "2"):
							kasaHareketleriOlustur.KasaAlacak   = float(replaceTutar)
						kasaHareketleriOlustur.Aciklama     = ajaxAciklama
						kasaHareketleriOlustur.CariKodu     = ajaxCariUnvani
						kasaHareketleriOlustur.save()
						ajaxMesaj = "1"
						try:
							# Fatura Kaydı Yapıldıktan Sonra MakbuzNoModel Tablosundan Makbuz Numarasını Arttırma
							sqlTahMakNoGuncelle = get_object_or_404(MakbuzNo,KasaKodu=ajaxKasaKodu)
							if(ajaxMakbuz == "1"):
								sqlTahMakNoGuncelle.TahsilatMakbuzuNo = int(ajaxMakbuzNo) + 1
								sqlTahMakNoGuncelle.save()
							if(ajaxMakbuz == "2"):
								sqlTahMakNoGuncelle.TediyeMakbuzuNo = int(ajaxMakbuzNo) + 1
								sqlTahMakNoGuncelle.save()
						except:
							pass	
						try:
							# Seçilen Makbuza Göre Kasa Bakiyesini Güncelleme
							kasaGuncelle = get_object_or_404(Kasa, KasaKodu=ajaxKasaKodu)
							if(ajaxMakbuz == "1"):
								kasaGuncelle.KasaBorc = float(kasaGuncelle.KasaBorc) + float(replaceTutar)
								kasaGuncelle.save()
							if(ajaxMakbuz == "2"):
								kasaGuncelle.KasaAlacak = float(kasaGuncelle.KasaAlacak) + float(replaceTutar)
								kasaGuncelle.save()
						except:
							pass	
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"
					context = {"ajaxMesaj" : ajaxMesaj,}	
					return JsonResponse(context)	
				sqlKasa = Kasa.objects.filter(IsDeleted=False)
				sqlCari = Cari.objects.filter(IsDeleted=False)
				context = {
					"modulYetkisi" : modulYetkisi,
					"suan"		   : suan,
					"sqlCari" 	   : sqlCari,
					"sqlKasa"      : sqlKasa,
				}
				return render (request, "kasa/kasaharolustur.html", context)
			else:		
				messages.success(request, "Kasa Hareketleri Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def KasaHareketleriListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if (modulYetkisi.IsKasa == True):
			islemlerKontrol = get_object_or_404(KasaHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKasaHareketleriListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlKasaHareketleri = get_object_or_404(KasaHareketleri, id=ajaxDetay)
						if(sqlKasaHareketleri.Makbuz == "1"):
							varMakbuz = "Tahsilat Makbuzu"
						if(sqlKasaHareketleri.Makbuz == "2"):
							varMakbuz = "Tediye Makbuzu"
						if(sqlKasaHareketleri.Makbuz == "3"):
							varMakbuz = "Kasa Açılış Fişi"		
						context = {
							"ajaxKasaKodu"     : sqlKasaHareketleri.KasaKodu,
							"ajaxMakbuz"       : varMakbuz,
							"ajaxMakbuzNo"     : sqlKasaHareketleri.MakbuzNo,
							"ajaxMakbuzTarihi" : sqlKasaHareketleri.MakbuzTarihi,
							"ajaxKasaBorc"     : sqlKasaHareketleri.KasaBorc,
							"ajaxKasaAlacak"   : sqlKasaHareketleri.KasaAlacak,
							"ajaxCariUnvani"   : sqlKasaHareketleri.CariKodu,
						}
						return JsonResponse(context)
					ajaxIptal = request.POST.get("ajaxIptal")
					if(ajaxIptal):
						sqlKasaHareketleriIptal = get_object_or_404(KasaHareketleri, id=ajaxIptal)
						sqlKasaHareketleriIptal.IsCanceled = True
						sqlKasaHareketleriIptal.save()
						try:
							kasaGuncelle = get_object_or_404(Kasa, KasaKodu=sqlKasaHareketleriIptal.KasaKodu)
							if(sqlKasaHareketleriIptal.Makbuz == "1"):
								kasaGuncelle.KasaBorc = float(kasaGuncelle.KasaBorc) - float(sqlKasaHareketleriIptal.KasaBorc)
								kasaGuncelle.save()
							if(sqlKasaHareketleriIptal.Makbuz == "2"):
								kasaGuncelle.KasaAlacak = float(kasaGuncelle.KasaAlacak) - float(sqlKasaHareketleriIptal.KasaAlacak)
								kasaGuncelle.save()
						except:
							pass
						# KAT = Kasalarlar Arası Transfer	
						try:
							kasaGuncelleKAT = get_object_or_404(Kasa, KasaKodu=sqlKasaHareketleriIptal.CariKodu)
							if(sqlKasaHareketleriIptal.Makbuz == "1"):
								kasaGuncelleKAT.KasaAlacak = float(kasaGuncelleKAT.KasaAlacak) - float(sqlKasaHareketleriIptal.KasaBorc)
								kasaGuncelleKAT.save()
							if(sqlKasaHareketleriIptal.Makbuz == "2"):
								kasaGuncelleKAT.KasaBorc = float(kasaGuncelleKAT.KasaBorc) - float(sqlKasaHareketleriIptal.KasaAlacak)
								kasaGuncelleKAT.save()
						except:
							pass	
						context = {"ajaxMesaj" : "Başarılı"}
						return JsonResponse(context)
					ajaxSil = request.POST.get('ajaxSil')
					if(ajaxSil):
						sqlKasaHareketleriSil = get_object_or_404(KasaHareketleri, id=ajaxSil)
						sqlKasaHareketleriSil.IsDeleted = True
						sqlKasaHareketleriSil.save()
						context = {"ajaxMesaj"     : "Başarılı",}
						return JsonResponse(context)		
				sqlKasaHareketleri = KasaHareketleri.objects.filter(IsCanceled=False)
				sqlKasaHareketleriIsCanceled = KasaHareketleri.objects.filter(IsCanceled=True,IsDeleted=False)
				context = {
					"modulYetkisi"                 : modulYetkisi,
					"islemlerKontrol"              : islemlerKontrol,
					"suan"				           : suan,
					"sqlKasaHareketler"	           : sqlKasaHareketleri,
					"sqlKasaHareketleriIsCanceled" : sqlKasaHareketleriIsCanceled,
				}
				return render (request, "kasa/kasahareketleri.html", context)
			else:		
				messages.success(request, "Kasa Hareketleri Listesini Görüntüleme Yetkiniz Yok !")
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
		if (modulYetkisi.IsKasa == True):
			islemlerKontrol = get_object_or_404(KasaHareketleriYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKasaHareketleriOlustur == True):
				if request.is_ajax():
					ajaxMakbuzKontrol = request.POST.get("ajaxMakbuzKontrol")
					ajaxTahMakNoKasa  = request.POST.get("ajaxTahMakNoKasa")
					ajaxTedMakNoKasa  = request.POST.get("ajaxTedMakNoKasa")
					if(ajaxMakbuzKontrol):
						if(ajaxMakbuzKontrol == "1"):
							makbuzNo = ""
							try:
								sqlKasaKontrol = get_object_or_404(Kasa,KasaKodu=ajaxTahMakNoKasa)
								try:
									sqlMakbuzNo = get_object_or_404(MakbuzNo,KasaKodu=ajaxTahMakNoKasa)
									if(sqlMakbuzNo.TahsilatMakbuzuNo != ""):
										makbuzNo = sqlMakbuzNo.TahsilatMakbuzuNo
									else:
										makbuzNo = None				
								except:
									makbuzNo = None
							except:
									makbuzNo = False		
							context = {"ajaxSqlMakbuzNo" : makbuzNo,}
							return JsonResponse(context)
						if(ajaxMakbuzKontrol == "2"):
							makbuzNo = ""
							try:
								sqlKasaKontrol = get_object_or_404(Kasa,KasaKodu=ajaxTedMakNoKasa)
								try:
									sqlTedMakNo = get_object_or_404(MakbuzNo,KasaKodu=ajaxTedMakNoKasa)
									if(sqlTedMakNo.TediyeMakbuzuNo != ""):
										makbuzNo = sqlTedMakNo.TediyeMakbuzuNo
									else:
										makbuzNo = None
								except:
									makbuzNo = None
							except:
									makbuzNo = False		
							context = {"ajaxSqlMakbuzNo" : makbuzNo,}
							return JsonResponse(context)

					ajaxBakiyeKontrol   = request.POST.get("ajaxBakiyeKontrol")
					ajaxKasaKoduKontrol	= request.POST.get("ajaxKasaKoduKontrol")
					if(ajaxBakiyeKontrol):
						replaceBakiyeKontrol = ajaxBakiyeKontrol.replace(",",".")
						sqlKasaAdi = get_object_or_404(Kasa,KasaKodu=ajaxKasaKoduKontrol)
						if(float(sqlKasaAdi.KasaBorc - sqlKasaAdi.KasaAlacak) - float(replaceBakiyeKontrol) < 0):
							ajaxMesaj = "Yetersiz Bakiye !"
						else:
							ajaxMesaj = None
						context = {"ajaxMesaj" : ajaxMesaj}
						return JsonResponse(context)
				
					ajaxBorcHesabi   = request.POST.get("ajaxBorcHesabi")
					ajaxAlacakHesabi = request.POST.get("ajaxAlacakHesabi")
					ajaxMakbuz       = request.POST.get("ajaxMakbuz")
					ajaxMakbuzNo     = request.POST.get("ajaxMakbuzNo")
					ajaxMakbuzTarihi = request.POST.get("ajaxMakbuzTarihi")
					ajaxTutar        = request.POST.get("ajaxTutar")
					ajaxAciklama     = request.POST.get("ajaxAciklama")	
					if(ajaxBorcHesabi != "" and ajaxAlacakHesabi != "" and ajaxMakbuz != "" and ajaxMakbuzNo != "" and ajaxMakbuzTarihi != "" and ajaxTutar != ""):
						replaceTutar = ajaxTutar.replace(",",".")
						if(ajaxMakbuz == "1"):
							try:
								tedMakNoOto = get_object_or_404(MakbuzNo,KasaKodu=ajaxAlacakHesabi)
								if(tedMakNoOto.TediyeMakbuzuNo != "" or tedMakNoOto.TediyeMakbuzuNo != None):
									kasaBorcOlustur = KasaHareketleri()
									kasaBorcOlustur.KasaKodu     = ajaxBorcHesabi
									kasaBorcOlustur.Makbuz       = ajaxMakbuz
									kasaBorcOlustur.MakbuzNo     = ajaxMakbuzNo
									kasaBorcOlustur.MakbuzTarihi = ajaxMakbuzTarihi
									kasaBorcOlustur.KasaBorc     = float(replaceTutar)
									kasaBorcOlustur.Aciklama     = ajaxAciklama
									kasaBorcOlustur.CariKodu     = ajaxAlacakHesabi
									kasaBorcOlustur.save()
									kasaAlacakOlusturOto = KasaHareketleri()
									kasaAlacakOlusturOto.KasaKodu     = ajaxAlacakHesabi
									kasaAlacakOlusturOto.Makbuz       = "2"
									kasaAlacakOlusturOto.MakbuzNo     = tedMakNoOto.TediyeMakbuzuNo
									kasaAlacakOlusturOto.MakbuzTarihi = ajaxMakbuzTarihi
									kasaAlacakOlusturOto.KasaAlacak   = float(replaceTutar)
									kasaAlacakOlusturOto.Aciklama     = "Ödeme Yapıldı"
									kasaAlacakOlusturOto.CariKodu     = ajaxBorcHesabi
									kasaAlacakOlusturOto.save()
									tedMakNoOto.TediyeMakbuzuNo = int(tedMakNoOto.TediyeMakbuzuNo) + 1
									tedMakNoOto.save()
									ajaxMesaj = "1"
									try:
										sqlTahMakNoGuncelle = get_object_or_404(MakbuzNo,KasaKodu=ajaxBorcHesabi)
										sqlTahMakNoGuncelle.TahsilatMakbuzuNo = int(ajaxMakbuzNo) + 1
										sqlTahMakNoGuncelle.save()			
									except:
										pass
									try:
										kasaGuncelleBorc = get_object_or_404(Kasa, KasaKodu=ajaxBorcHesabi)
										kasaGuncelleBorc.KasaBorc = float(kasaGuncelleBorc.KasaBorc) + float(replaceTutar)
										kasaGuncelleBorc.save()
									except:
										pass	
									try:
										kasaGuncelleAlacak = get_object_or_404(Kasa, KasaKodu=ajaxAlacakHesabi)
										kasaGuncelleAlacak.KasaAlacak = float(kasaGuncelleAlacak.KasaAlacak) + float(replaceTutar)
										kasaGuncelleAlacak.save()
									except:
										pass	
								else:
									ajaxMesaj = False	
							except:
								ajaxMesaj = False
						if(ajaxMakbuz == "2"):
							try:
								tahMakNoOto = get_object_or_404(MakbuzNo,KasaKodu=ajaxBorcHesabi)
								if(tahMakNoOto.TahsilatMakbuzuNo != "" or tahMakNoOto.TahsilatMakbuzuNo != None):
									kasaAlacakOlustur = KasaHareketleri()
									kasaAlacakOlustur.KasaKodu     = ajaxAlacakHesabi
									kasaAlacakOlustur.Makbuz       = ajaxMakbuz
									kasaAlacakOlustur.MakbuzNo     = ajaxMakbuzNo
									kasaAlacakOlustur.MakbuzTarihi = ajaxMakbuzTarihi
									kasaAlacakOlustur.KasaAlacak   = float(replaceTutar)
									kasaAlacakOlustur.Aciklama     = ajaxAciklama
									kasaAlacakOlustur.CariKodu     = ajaxBorcHesabi
									kasaAlacakOlustur.save()
									kasaBorcOlusturOto = KasaHareketleri()
									kasaBorcOlusturOto.KasaKodu     = ajaxBorcHesabi
									kasaBorcOlusturOto.Makbuz       = "1"
									kasaBorcOlusturOto.MakbuzNo     = tahMakNoOto.TahsilatMakbuzuNo
									kasaBorcOlusturOto.MakbuzTarihi = ajaxMakbuzTarihi
									kasaBorcOlusturOto.KasaBorc     = float(replaceTutar)
									kasaBorcOlusturOto.Aciklama     = "Ödeme Alındı"
									kasaBorcOlusturOto.CariKodu     = ajaxAlacakHesabi
									kasaBorcOlusturOto.save()
									tahMakNoOto.TahsilatMakbuzuNo = int(tahMakNoOto.TahsilatMakbuzuNo) + 1
									tahMakNoOto.save()
									ajaxMesaj = "1"
									try:
										sqlTedMakNoGuncelle = get_object_or_404(MakbuzNo,KasaKodu=ajaxAlacakHesabi)
										sqlTedMakNoGuncelle.TediyeMakbuzuNo = int(ajaxMakbuzNo) + 1
										sqlTedMakNoGuncelle.save()
									except:
										pass
									try:
										kasaGuncelleAlacak = get_object_or_404(Kasa, KasaKodu=ajaxAlacakHesabi)
										kasaGuncelleAlacak.KasaAlacak = float(kasaGuncelleAlacak.KasaAlacak) + float(replaceTutar)
										kasaGuncelleAlacak.save()
									except:
										pass
									try:
										kasaGuncelleBorc = get_object_or_404(Kasa, KasaKodu=ajaxBorcHesabi)
										kasaGuncelleBorc.KasaBorc = float(kasaGuncelleBorc.KasaBorc) + float(replaceTutar)
										kasaGuncelleBorc.save()
									except:
										pass	
								else:
									ajaxMesaj = False
							except:
								ajaxMesaj = False					
					else:	
						ajaxMesaj = "Lüften Formu Boş Bırakmayınız !"			
					context = {"ajaxMesaj":ajaxMesaj,}
					return JsonResponse(context)

				sqlKasa = Kasa.objects.filter(IsDeleted=False)
				sqlBanka = Banka.objects.filter(IsDeleted=False)
				context = {
					"modulYetkisi" : modulYetkisi,
					"sqlBanka"	   : sqlBanka,
					"sqlKasa"	   : sqlKasa,
					"suan"		   : suan,
				}
				return render (request, "kasa/transfer.html", context)
			else:		
				messages.success(request, "Kasa Hareketleri Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.danger(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def Tanimlamalar(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if (modulYetkisi.IsKasa == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsKasaTanimlamalari == True):
				if request.is_ajax():
					ajaxKasaSecimi       = request.POST.get("ajaxKasaSecimi")
					if(ajaxKasaSecimi):
						try:
							sqlKasaMakbuzNo = get_object_or_404(MakbuzNo,KasaKodu=ajaxKasaSecimi)
							sqlTahMakNo = sqlKasaMakbuzNo.TahsilatMakbuzuNo
							sqlTedMakNo = sqlKasaMakbuzNo.TediyeMakbuzuNo
						except:
							sqlTahMakNo = "" 
							sqlTedMakNo   = ""
						context = {
							"ajaxKasaTahDek" : sqlTahMakNo,
							"ajaxKasaTedDek" : sqlTedMakNo,
							}
						return JsonResponse(context)
					ajaxKasaKodu = request.POST.get("ajaxKasaKodu")
					ajaxTahMakNo = request.POST.get("ajaxTahMakNo")
					ajaxTedMakNo = request.POST.get("ajaxTedMakNo")
					try:
						sqlMakbuzNoModel = get_object_or_404(MakbuzNo,KasaKodu=ajaxKasaKodu)
						if(ajaxTahMakNo != ""):
							sqlMakbuzNoModel.TahsilatMakbuzuNo = ajaxTahMakNo
							sqlMakbuzNoModel.save()
						if(ajaxTedMakNo != ""):
							sqlMakbuzNoModel.TediyeMakbuzuNo = ajaxTedMakNo
							sqlMakbuzNoModel.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !"}
						return JsonResponse(context)
					except:
						sqlMakbuzNoOlustur = MakbuzNo()
						if(ajaxTahMakNo != ""):
							sqlMakbuzNoOlustur.KasaKodu          = ajaxKasaKodu
							sqlMakbuzNoOlustur.TahsilatMakbuzuNo = ajaxTahMakNo
							sqlMakbuzNoOlustur.save()
						if(ajaxTedMakNo != ""):
							sqlMakbuzNoOlustur.KasaKodu        = ajaxKasaKodu
							sqlMakbuzNoOlustur.TediyeMakbuzuNo = ajaxTedMakNo
							sqlMakbuzNoOlustur.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !"}
						return JsonResponse(context)
				kasalar = Kasa.objects.all()	
				context = {
					"modulYetkisi" : modulYetkisi,
					"kasalar"      : kasalar,
				}		
				return render (request, "kasa/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")