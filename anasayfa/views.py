from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from django.shortcuts import render
from kullanicilar.encryption import encryption_h
from django.utils import timezone
from django.http import JsonResponse


def AnasayfaView(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsAnaSayfa == True):
			if request.is_ajax():
				duyuruIcerik      = None
				gorevIcerik       = None
				hatirlatmaIcerik = None
				ajaxDuyuruKey    = request.POST.get("ajaxDuyuruKey")
				ajaxDuyuruKodu	 = request.POST.get("ajaxDuyuruKodu")
				if(ajaxDuyuruKey == "1"):
					sqlDuyuru = get_object_or_404(Duyurular,DuyuruKodu=ajaxDuyuruKodu)
					duyuruIcerik = sqlDuyuru.Icerik
				ajaxGorevKey    = request.POST.get("ajaxGorevKey")
				ajaxGorevKodu	 = request.POST.get("ajaxGorevKodu")
				if(ajaxGorevKey == "1"):
					sqlGorev = get_object_or_404(Gorevler,GorevKodu=ajaxGorevKodu)
					gorevIcerik = sqlGorev.Icerik
				ajaxHatirlatmaKey    = request.POST.get("ajaxHatirlatmaKey")
				ajaxHatirlatmaKodu	 = request.POST.get("ajaxHatirlatmaKodu")
				if(ajaxHatirlatmaKey == "1"):
					sqlHatirlatma = get_object_or_404(Hatirlatmalar,HatirlatmaKodu=ajaxHatirlatmaKodu)
					hatirlatmaIcerik = sqlHatirlatma.Icerik
				context = {
					"ajaxDuyuru"     : duyuruIcerik,
					"ajaxGorev"	     : gorevIcerik,
					"ajaxHatirlatma" : hatirlatmaIcerik,
				}
				return JsonResponse(context)		
			suan = timezone.now()
			
			sqlDuyurular = []
			for sqlDuyurularK in Duyurular.objects.filter(Kullanici=kullaniciKontrol.KullaniciKodu):
				duyurularDemet = {"DuyuruKodu": sqlDuyurularK.DuyuruKodu,"Baslik":sqlDuyurularK.Baslik,"Icerik":sqlDuyurularK.Icerik,"KullaniciGrubu":sqlDuyurularK.KullaniciGrubu,"Kullanici":sqlDuyurularK.Kullanici,"Durumu":sqlDuyurularK.Durumu}
				sqlDuyurular.append(duyurularDemet)
			for sqlDuyurularKG in Duyurular.objects.filter(KullaniciGrubu=kullaniciKontrol.KullaniciGrubu):
				if(sqlDuyurularKG.KullaniciGrubu != ""):
					duyurularDemet = {"DuyuruKodu": sqlDuyurularKG.DuyuruKodu,"Baslik":sqlDuyurularKG.Baslik,"Icerik":sqlDuyurularKG.Icerik,"KullaniciGrubu":sqlDuyurularKG.KullaniciGrubu,"Kullanici":sqlDuyurularKG.Kullanici,"Durumu":sqlDuyurularKG.Durumu}
					sqlDuyurular.append(duyurularDemet)

			sqlGorevler = []
			for sqlGorevlerK in Gorevler.objects.filter(Durumu=1,Kullanici=kullaniciKontrol.KullaniciKodu):
				gorevlerDemet = {"GorevKodu": sqlGorevlerK.GorevKodu,"Baslik":sqlGorevlerK.Baslik,"Icerik":sqlGorevlerK.Icerik,"KullaniciGrubu":sqlGorevlerK.KullaniciGrubu,"Kullanici":sqlGorevlerK.Kullanici,"Durumu":sqlGorevlerK.Durumu}
				sqlGorevler.append(gorevlerDemet)
			for sqlGorevlerKG in Gorevler.objects.filter(Durumu=1,KullaniciGrubu=kullaniciKontrol.KullaniciGrubu):
				if(sqlGorevlerKG.KullaniciGrubu != ""):
					gorevlerDemet = {"GorevKodu": sqlGorevlerKG.GorevKodu,"Baslik":sqlGorevlerKG.Baslik,"Icerik":sqlGorevlerKG.Icerik,"KullaniciGrubu":sqlGorevlerKG.KullaniciGrubu,"Kullanici":sqlGorevlerKG.Kullanici,"Durumu":sqlGorevlerKG.Durumu}
					sqlGorevler.append(gorevlerDemet)
			
			sqlHatirlatmalar = []
			for sqlHatirlatmalarK in Hatirlatmalar.objects.filter(Kullanici=kullaniciKontrol.KullaniciKodu):
				hatirlatmalarDemet = {"HatirlatmaKodu": sqlHatirlatmalarK.HatirlatmaKodu,"Baslik":sqlHatirlatmalarK.Baslik,"Icerik":sqlHatirlatmalarK.Icerik,"KullaniciGrubu":sqlHatirlatmalarK.KullaniciGrubu,"Kullanici":sqlHatirlatmalarK.Kullanici,"Durumu":sqlHatirlatmalarK.Durumu}
				sqlHatirlatmalar.append(hatirlatmalarDemet)
			for sqlHatirlatmalarKG in Hatirlatmalar.objects.filter(KullaniciGrubu=kullaniciKontrol.KullaniciGrubu):
				if(sqlHatirlatmalarKG.KullaniciGrubu != ""):
					hatirlatmalarDemet = {"HatirlatmaKodu": sqlHatirlatmalarKG.HatirlatmaKodu,"Baslik":sqlHatirlatmalarKG.Baslik,"Icerik":sqlHatirlatmalarKG.Icerik,"KullaniciGrubu":sqlHatirlatmalarKG.KullaniciGrubu,"Kullanici":sqlHatirlatmalarKG.Kullanici,"Durumu":sqlHatirlatmalarKG.Durumu}
					sqlHatirlatmalar.append(hatirlatmalarDemet)

			context = {
				"modulYetkisi"     : modulYetkisi,
				"suan"             : suan,
				"sqlDuyurular"	   : sqlDuyurular,
				"sqlGorevler"      : sqlGorevler,
				"sqlHatirlatmalar" : sqlHatirlatmalar,
			}
			return render (request, "anasayfa/anasayfa.html",context)
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			print("Yetkisiz Kullanıcı")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect ("kullanicilar:giris")

def KullaniciIslemlerim(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session['KullaniciKodu'],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsAnaSayfa == True):
			sqlKullanici = get_object_or_404(Kullanicilar,KullaniciKodu=kullaniciKontrol.KullaniciKodu)
			if request.is_ajax():
				ajaxKullaniciAdi	 = request.POST.get("ajaxKullaniciAdi")
				ajaxKullaniciParola  = request.POST.get("ajaxKullaniciParola")
				ajaxKullaniciParolaD = request.POST.get("ajaxKullaniciParolaD")
				if(ajaxKullaniciParola == ajaxKullaniciParolaD):
					encryptionParola = encryption_h(ajaxKullaniciAdi, ajaxKullaniciParola)
					sqlKullanici.KullaniciAdi    = ajaxKullaniciAdi
					sqlKullanici.KullaniciParola = encryptionParola
					sqlKullanici.save()
					context = {"ajaxMesaj":"Kayıt Başarılı !",}
					return JsonResponse(context)
			context = {
				"modulYetkisi" : modulYetkisi,
				"sqlKullanici" : sqlKullanici,
			}
			return render(request, "anasayfa/islemlerim.html",context)	
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
		if(modulYetkisi.IsAnaSayfa == True):
			suan = timezone.now()
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsAnasayfaTanimlamalari == True):
				if request.is_ajax():
					ajaxDuyuruKodu       = request.POST.get("ajaxDuyuruKodu")
					ajaxDuyuruBaslik     = request.POST.get("ajaxDuyuruBaslik")
					ajaxDuyuruIcerik     = request.POST.get("ajaxDuyuruIcerik")
					ajaxDuyuruKullanici  = request.POST.get("ajaxDuyuruKullanici")
					ajaxDuyuruKullaniciG = request.POST.get("ajaxDuyuruKullaniciG")
					
					ajaxGorevKodu       = request.POST.get("ajaxGorevKodu")
					ajaxGorevBaslik     = request.POST.get("ajaxGorevBaslik")
					ajaxGorevIcerik     = request.POST.get("ajaxGorevIcerik")
					ajaxGorevKullanici  = request.POST.get("ajaxGorevKullanici")
					ajaxGorevKullaniciG = request.POST.get("ajaxGorevKullaniciG")

					ajaxHatirlatmaKodu       = request.POST.get("ajaxHatirlatmaKodu")
					ajaxHatirlatmaBaslik     = request.POST.get("ajaxHatirlatmaBaslik")
					ajaxHatirlatmaIcerik     = request.POST.get("ajaxHatirlatmaIcerik")
					ajaxHatirlatmaKullanici  = request.POST.get("ajaxHatirlatmaKullanici")
					ajaxHatirlatmaKullaniciG = request.POST.get("ajaxHatirlatmaKullaniciG")
					
					if (ajaxDuyuruKodu):
						sqlDuyurular = Duyurular()
						sqlDuyurular.DuyuruKodu 	= ajaxDuyuruKodu
						sqlDuyurular.Baslik 		= ajaxDuyuruBaslik
						sqlDuyurular.Icerik 		= ajaxDuyuruIcerik
						sqlDuyurular.Durumu 		= 1
						sqlDuyurular.Kullanici      = ajaxDuyuruKullanici
						sqlDuyurular.KullaniciGrubu = ajaxDuyuruKullaniciG
						sqlDuyurular.save()
						context = {"ajaxMesaj": "Başarılı!",}
						return JsonResponse(context)
					if (ajaxGorevKodu):
						sqlGorevler = Gorevler()
						sqlGorevler.GorevKodu      = ajaxGorevKodu
						sqlGorevler.Baslik         = ajaxGorevBaslik
						sqlGorevler.Icerik         = ajaxGorevIcerik
						sqlGorevler.Durumu         = 1
						sqlGorevler.Kullanici      = ajaxGorevKullanici
						sqlGorevler.KullaniciGrubu = ajaxGorevKullaniciG
						sqlGorevler.save()
						context = {"ajaxMesaj": "Başarılı!",}
						return JsonResponse(context)
					if (ajaxHatirlatmaKodu):
						sqlHatirlatmalar = Hatirlatmalar()
						sqlHatirlatmalar.HatirlatmaKodu = ajaxHatirlatmaKodu
						sqlHatirlatmalar.Baslik         = ajaxHatirlatmaBaslik
						sqlHatirlatmalar.Icerik         = ajaxHatirlatmaIcerik
						sqlHatirlatmalar.Durumu         = 1
						sqlHatirlatmalar.Kullanici      = ajaxHatirlatmaKullanici
						sqlHatirlatmalar.KullaniciGrubu = ajaxHatirlatmaKullaniciG
						sqlHatirlatmalar.save()
						context = {"ajaxMesaj": "Başarılı!",}
						return JsonResponse(context)		
				sqlKullaniciGrubu = KullaniciGrubuModel.objects.all()
				sqlKullanicilar = Kullanicilar.objects.filter(IsDeleted=False)		
				context = {
					"modulYetkisi"      : modulYetkisi,
					"suan"              : suan,
					"sqlKullaniciGrubu" : sqlKullaniciGrubu,
					"sqlKullanicilar" 	: sqlKullanicilar,
				}
				return render (request, "anasayfa/tanimlamalar.html",context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")		
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect ("kullanicilar:giris")			