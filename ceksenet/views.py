from kullanicilar.views import *
from kullanicilar.models import *
from .models import *
from cari.models import *
from fatura.models import *
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

suan = timezone.now()
def CekBordroOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCekSenet == True):
			islemlerKontrol = get_object_or_404(CekSenetYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsCekBordroOlustur == True):
				if request.is_ajax():
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						try:
							sqlCekSil = get_object_or_404(Cek, id=ajaxSil)
							sqlCekSil.delete()
							context = {"ajaxMesaj": "Silme İşlemi Başarılı!",}
							return JsonResponse(context)
						except:
							pass

					ajaxCekKontrol   = request.POST.get("ajaxCekKontrol")
					if(ajaxCekKontrol):
						try:
							sqlCekNoModel = get_object_or_404(OdemeAraciNoModel,id="1")
							if(ajaxCekKontrol == "2"):
								if(sqlCekNoModel.CekNo != ""):
									cekNoModel = sqlCekNoModel.CekNo
								else:
									cekNoModel = ""		
						except:
							cekNoModel = ""
						context = {"ajaxCekNoModel" : cekNoModel,}
						return JsonResponse(context)

					ajaxKaydet = request.POST.get("ajaxKaydet")
					if(ajaxKaydet):
						try:
							for cekIsSaved in Cek.objects.filter(BordroNo=ajaxKaydet):
								cekIsSaved.IsSaved = True
								cekIsSaved.save()
							try:
								sqlBordroNoGuncelle = get_object_or_404(OdemeAraciNoModel,id="1")
								sqlBordroNoGuncelle.BordroNo = int(sqlBordroNoGuncelle.BordroNo) + 1
								sqlBordroNoGuncelle.save()
							except:
								pass	
							context = {"ajaxMesaj": "1",}
							return JsonResponse(context)
						except:
							context = {"ajaxMesaj": "Hata !",}
							return JsonResponse(context)

					ajaxDurum        = request.POST.get("ajaxDurum")
					ajaxCekNo 		 = request.POST.get("ajaxCekNo")
					ajaxIslemTuru    = request.POST.get("ajaxIslemTuru")
					ajaxBordroNo     = request.POST.get("ajaxBordroNo")
					ajaxBordroTarihi = request.POST.get("ajaxBordroTarihi")
					ajaxCariUnvani   = request.POST.get("ajaxCariUnvani")
					ajaxVade 		 = request.POST.get("ajaxVade")
					ajaxOdemeYeri 	 = request.POST.get("ajaxOdemeYeri")
					ajaxDoviz 		 = request.POST.get("ajaxDoviz")
					ajaxTutar 		 = request.POST.get("ajaxTutar")
					ajaxBankaAdi 	 = request.POST.get("ajaxBankaAdi")
					ajaxSubeKodu 	 = request.POST.get("ajaxSubeKodu")
					ajaxHesapNo 	 = request.POST.get("ajaxHesapNo")
					tutarReplace     = ajaxTutar.replace(",",".")
					if(ajaxCekNo != "" and ajaxIslemTuru != "" and ajaxBordroNo != "" and ajaxBordroTarihi != "" and ajaxCariUnvani != "" and ajaxVade != "" and ajaxOdemeYeri != "" and ajaxDoviz != "" and ajaxTutar != "" and ajaxBankaAdi != "" and ajaxSubeKodu != "" and ajaxHesapNo != ""):
						sqlCekOlustur = Cek()
						if(ajaxDurum == "5"):
							sqlCekOlustur.Durum = ajaxIslemTuru
							sqlCekIsTransferCache = get_object_or_404(Cek,CekNo=ajaxCekNo,Tipi="1")
							sqlCekIsTransferCache.Durum = ajaxIslemTuru
							sqlCekIsTransferCache.IsTransferCache = True
							sqlCekIsTransferCache.save()
						else:
							sqlCekOlustur.Durum = "5"
						sqlCekOlustur.Tipi         = ajaxIslemTuru
						sqlCekOlustur.BordroNo     = ajaxBordroNo
						sqlCekOlustur.BordroTarihi = ajaxBordroTarihi
						sqlCekOlustur.CariKodu     = ajaxCariUnvani
						sqlCekOlustur.CekNo        = ajaxCekNo
						sqlCekOlustur.Vade         = ajaxVade
						sqlCekOlustur.OdemeYeri    = ajaxOdemeYeri
						sqlCekOlustur.Doviz        = ajaxDoviz
						sqlCekOlustur.Tutar        = tutarReplace
						sqlCekOlustur.BankaAdi     = ajaxBankaAdi
						sqlCekOlustur.SubeKodu     = ajaxSubeKodu
						sqlCekOlustur.HesapNo      = ajaxHesapNo
						sqlCekOlustur.save()
						ajaxMesaj = "1"
						try:
							cekNoGuncelle = get_object_or_404(OdemeAraciNoModel,id="1")
							cekNo = ""
							if(ajaxIslemTuru == "2"):
								cekNoGuncelle.CekNo = int(ajaxCekNo) + 1
								cekNoGuncelle.save()
								cekNo = cekNoGuncelle.CekNo
						except:
							pass		
						sqlCek = Cek.objects.filter(BordroNo=sqlCekOlustur.BordroNo)
						for cek in sqlCek:
							pass
						context = {
							"ajaxMesaj"        : ajaxMesaj,
							"ajaxId"           : str(cek.id),
					        "ajaxIslemTuru"    : cek.Tipi,
							"ajaxBordroNo"     : cek.BordroNo,
							"ajaxBordroTarihi" : str(cek.BordroTarihi),
							"ajaxCariUnvani"   : cek.CariKodu,
							"ajaxCekNo"        : cek.CekNo,
							"ajaxVade"         : str(cek.Vade),
							"ajaxOdemeYeri"    : cek.OdemeYeri,
							"ajaxDoviz"        : cek.Doviz,
							"ajaxTutar"        : str(cek.Tutar),
							"ajaxBankaAdi"     : cek.BankaAdi,
							"ajaxSubeKodu"     : cek.SubeKodu,
							"ajaxHesapNo"      : cek.HesapNo,
							"ajaxGuncelCekNo"  : cekNo,
						}	
						return JsonResponse(context)
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"	
					context = {"ajaxMesaj" : ajaxMesaj}
					return JsonResponse(context)	
				try:
					sqlCekIsTransferred = get_object_or_404(Cek, IsTransferred=True)
					sqlCekIsTransferred.IsTransferred = False
					sqlCekIsTransferred.save()
					key = 1
				except:
					sqlCekIsTransferred = ""
					key = 0
				try:
					sqlBordroNo = get_object_or_404(OdemeAraciNoModel,id="1")
				except:
					sqlBordroNo = ""
				try:
					for bordroIsDeleted in Cek.objects.filter(IsSaved=False):
						bordroIsDeleted.delete()
				except:
					pass			
				sqlCari = Cari.objects.all()
				context = {
					"suan"                : suan,
					"modulYetkisi"        : modulYetkisi,
					"sqlCari"             : sqlCari,
					"sqlBordroNo"         : sqlBordroNo,
					"sqlCekIsTransferred" : sqlCekIsTransferred,
				}
				if(key == 0):
					return render (request, "ceksenet/cekbordro.html", context)
				if(key == 1):
					return render (request, "ceksenet/cekbordro2.html", context)		
			else:		
				messages.success(request, "Çek Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def SenetBordroOlustur(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCekSenet == True):
			islemlerKontrol = get_object_or_404(CekSenetYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsSenetBordroOlustur == True):
				if request.is_ajax():
					ajaxSil = request.POST.get("ajaxSil")
					if(ajaxSil):
						try:
							sqlSenetSil = get_object_or_404(Senet, id=ajaxSil)
							sqlSenetSil.delete()
							context = {"ajaxMesaj": "Silme İşlemi Başarılı!",}
							return JsonResponse(context)
						except:
							pass

					ajaxSenetKontrol   = request.POST.get("ajaxSenetKontrol")
					if(ajaxSenetKontrol):
						try:
							if(ajaxSenetKontrol == "2"):
								sqlSenetNoModel = get_object_or_404(OdemeAraciNoModel,id="1")
								if(sqlSenetNoModel.SenetNo != ""):
									senetNoModel = sqlSenetNoModel.SenetNo
								else:
									senetNoModel = ""		
						except:
							senetNoModel = ""
						context = {"ajaxSenetNoModel" : senetNoModel,}
						return JsonResponse(context)
					ajaxKaydet = request.POST.get("ajaxKaydet")
					if(ajaxKaydet):
						try:
							for bordroIsSaved in Senet.objects.filter(BordroNo=ajaxKaydet):
								bordroIsSaved.IsSaved = True
								bordroIsSaved.save()
							try:
								sqlBordroNoGuncelle = get_object_or_404(OdemeAraciNoModel,id="1")
								sqlBordroNoGuncelle.BordroNo = int(sqlBordroNoGuncelle.BordroNo) + 1
								sqlBordroNoGuncelle.save()
							except:
								pass	
							context = {"ajaxMesaj": "1",}
							return JsonResponse(context)
						except:
							context = {"ajaxMesaj": "Hata !",}
							return JsonResponse(context)

					ajaxDurum        = request.POST.get("ajaxDurum")
					ajaxSenetNo      = request.POST.get("ajaxSenetNo")
					ajaxIslemTuru    = request.POST.get("ajaxIslemTuru")
					ajaxBordroNo     = request.POST.get("ajaxBordroNo")
					ajaxBordroTarihi = request.POST.get("ajaxBordroTarihi")
					ajaxCariUnvani   = request.POST.get("ajaxCariUnvani")
					ajaxVade 		 = request.POST.get("ajaxVade")
					ajaxOdemeYeri 	 = request.POST.get("ajaxOdemeYeri")
					ajaxDoviz 		 = request.POST.get("ajaxDoviz")
					ajaxTutar 		 = request.POST.get("ajaxTutar")
					tutarReplace     = ajaxTutar.replace(",",".")
					if(ajaxSenetNo != "" and ajaxIslemTuru != "" and ajaxBordroNo != "" and ajaxBordroTarihi != "" and ajaxCariUnvani != "" and ajaxVade != "" and ajaxOdemeYeri != "" and ajaxDoviz != "" and ajaxTutar != ""):	
						sqlSenetOlustur = Senet()
						if(ajaxDurum == "5"):
							sqlSenetOlustur.Durum   = ajaxIslemTuru
							sqlSenetIsTransferCache = get_object_or_404(Senet,SenetNo=ajaxSenetNo,Tipi="1")
							sqlSenetIsTransferCache.Durum = ajaxIslemTuru
							sqlSenetIsTransferCache.IsTransferCache = True
							sqlSenetIsTransferCache.save()	
						else:
							sqlSenetOlustur.Durum    = "5"	
						sqlSenetOlustur.Tipi         = ajaxIslemTuru
						sqlSenetOlustur.BordroNo     = ajaxBordroNo
						sqlSenetOlustur.BordroTarihi = ajaxBordroTarihi
						sqlSenetOlustur.CariKodu     = ajaxCariUnvani
						sqlSenetOlustur.SenetNo      = ajaxSenetNo
						sqlSenetOlustur.Vade         = ajaxVade
						sqlSenetOlustur.OdemeYeri    = ajaxOdemeYeri
						sqlSenetOlustur.Doviz        = ajaxDoviz
						sqlSenetOlustur.Tutar        = tutarReplace
						sqlSenetOlustur.save()
						ajaxMesaj = "1"
						try:
							sqlSenetNoGuncelle = get_object_or_404(OdemeAraciNoModel,id="1")
							senetNo = ""
							if(ajaxIslemTuru == "2"):	
								sqlSenetNoGuncelle.SenetNo = int(ajaxSenetNo) + 1
								sqlSenetNoGuncelle.save()
								senetNo = sqlSenetNoGuncelle.SenetNo
						except:
							pass

						for senet in Senet.objects.filter(BordroNo=sqlSenetOlustur.BordroNo):
							pass
						context = {
							"ajaxMesaj"         : ajaxMesaj,
							"ajaxId"            : str(senet.id),
					        "ajaxIslemTuru"     : senet.Tipi,
							"ajaxBordroNo"      : senet.BordroNo,
							"ajaxBordroTarihi"  : str(senet.BordroTarihi),
							"ajaxCariUnvani"    : senet.CariKodu,
							"ajaxSenetNo"       : senet.SenetNo,
							"ajaxVade"          : str(senet.Vade),
							"ajaxOdemeYeri"     : senet.OdemeYeri,
							"ajaxDoviz"         : senet.Doviz,
							"ajaxTutar"         : str(senet.Tutar),
							"ajaxGuncelSenetNo" : senetNo,
						}	
						return JsonResponse(context)
					else:
						ajaxMesaj = "Lütfen Formu Boş Bırakmayınız !"	
					context = {"ajaxMesaj" : ajaxMesaj}
					return JsonResponse(context)	
				try:
					sqlSenetIsTransferred = get_object_or_404(Senet, IsTransferred=True)
					sqlSenetIsTransferred.IsTransferred = False
					sqlSenetIsTransferred.save()
					key = 1
				except:
					sqlSenetIsTransferred = ""
					key = 0
				try:
					sqlBordroNo = get_object_or_404(OdemeAraciNoModel,id="1")
				except:
					sqlBordroNo = ""
				try:
					for senetIsDeleted in Senet.objects.filter(IsSaved=False):
						senetIsDeleted.delete()
				except:
					pass			
				sqlCari = Cari.objects.all()
				context = {
					"suan"                  : suan,
					"modulYetkisi"          : modulYetkisi,
					"sqlCari"               : sqlCari,
					"sqlBordroNo"           : sqlBordroNo,
					"sqlSenetIsTransferred" : sqlSenetIsTransferred,
				}
				if(key == 0):
					return render (request, "ceksenet/senetbordro.html", context)
				if(key == 1):
					return render (request, "ceksenet/senetbordro2.html", context)		
			else:		
				messages.success(request, "Senet Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def CeklerListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCekSenet == True):
			islemlerKontrol = get_object_or_404(CekSenetYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsCekListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlCekler = get_object_or_404(Cek, id=ajaxDetay)
						if(sqlCekler.Tipi == "1"):
							cekTipi = "Çek Giriş(Alınan Çek)"
						if(sqlCekler.Tipi == "2"):	
							cekTipi = "Çek Çıkış(Cari Hesaba)"
						if(sqlCekler.Tipi == "3"):	
							cekTipi = "Çek Çıkış(Banka Tahsil)"
						if(sqlCekler.Tipi == "4"):	
							cekTipi = "Çek Çıkış(Banka Teminat)"
						if(sqlCekler.Doviz == "1"):
							doviz = "TL"
						if(sqlCekler.Doviz == "2"):
							doviz = "DOLAR"
						if(sqlCekler.Doviz == "3"):
							doviz = "EURO"
						if(sqlCekler.Durum == "1"):
							durum = "Çek Giriş(Alınan Çek)"
						if(sqlCekler.Durum == "2"):
							durum = "Çek Çıkış(Cari Hesaba)"
						if(sqlCekler.Durum == "3"):
							durum = "Çek Çıkış(Banka Tahsil)"
						if(sqlCekler.Durum == "4"):
							durum = "Çek Çıkış(Banka Teminat)"
						if(sqlCekler.Durum == "5"):
							durum = "Portföyde"
						context = {
							"ajaxBordroNo"     : sqlCekler.BordroNo,
							"ajaxBordroTarihi" : sqlCekler.BordroTarihi,
							"ajaxCekNo"        : sqlCekler.CekNo,
							"ajaxTipi"         : cekTipi,
							"ajaxDurum"        : durum,
							"ajaxVade"         : sqlCekler.Vade,
							"ajaxTutar"        : sqlCekler.Tutar,
							"ajaxDoviz"        : doviz,
							"ajaxCariKodu"     : sqlCekler.CariKodu,
							"ajaxBankaAdi"     : sqlCekler.BankaAdi,
							"ajaxSubeKodu"     : sqlCekler.SubeKodu,
							"ajaxHesapNo"      : sqlCekler.HesapNo,
							"ajaxOdemeYeri"    : sqlCekler.OdemeYeri,
						}
						return JsonResponse(context)

					ajaxCekIdIptal	= request.POST.get("ajaxCekIdIptal")
					if(ajaxCekIdIptal):
						sqlCekIptal = get_object_or_404(Cek,id=ajaxCekIdIptal)
						sqlCekIptal.IsCanceled = True
						sqlCekIptal.save()
						sqlCekDurumGuncelle = get_object_or_404(Cek,CekNo=sqlCekIptal.CekNo,Tipi="1",IsTransferCache=True)
						sqlCekDurumGuncelle.Durum = 5
						sqlCekDurumGuncelle.IsTransferCache = False
						sqlCekDurumGuncelle.save()
						context = {"ajaxMesaj": "İptal İşlemi Başarılı!",}
						return JsonResponse(context)

					ajaxCekNo   = request.POST.get("ajaxCekNo")
					ajaxCekTipi = request.POST.get("ajaxCekTipi")
					if(ajaxCekNo):
						try:
							sqlCekDurum = get_object_or_404(Cek,CekNo=ajaxCekNo,Tipi=ajaxCekTipi)
							sqlCekDurum.IsTransferred = True
							sqlCekDurum.Durum = "5"
							sqlCekDurum.save()
							context = {"ajaxMesaj": "İşlem Başarılı!",}
							return JsonResponse(context)
						except:
							pass
				sqlAlinanCekler  = Cek.objects.filter(Tipi=1,IsCanceled=False,Durum="5")
				sqlVerilenCekler = Cek.objects.filter(Tipi=2,IsCanceled=False)
				context = {
					"modulYetkisi" 	   : modulYetkisi,
					"islemlerKontrol"  : islemlerKontrol,
					"sqlAlinanCekler"  : sqlAlinanCekler,
					"sqlVerilenCekler" : sqlVerilenCekler,
				}
				return render (request, "ceksenet/ceklerlistele.html", context)		
			else:		
				messages.success(request, "Çekler Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")		

def SenetlerListele(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session["KullaniciKodu"],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCekSenet == True):
			islemlerKontrol = get_object_or_404(CekSenetYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsSenetListele == True):
				if request.is_ajax():
					ajaxDetay = request.POST.get("ajaxDetay")
					if(ajaxDetay):
						sqlSenetler = get_object_or_404(Senet, id=ajaxDetay)
						if(sqlSenetler.Tipi == "1"):	
							tipi = "Senet Giriş(Alınan Senet)"
						if(sqlSenetler.Tipi == "2"):	
							tipi = "Senet Çıkış(Cari Hesaba)"
						if(sqlSenetler.Tipi == "3"):	
							tipi = "Senet Çıkış(Banka Tahsil)"
						if(sqlSenetler.Tipi == "4"):	
							tipi = "Senet Çıkış(Banka Teminat)"
						if(sqlSenetler.Doviz == "1"):
							doviz = "TL"
						if(sqlSenetler.Doviz == "2"):
							doviz = "DOLAR"
						if(sqlSenetler.Doviz == "3"):
							doviz = "EURO"
						if(sqlSenetler.Durum == "1"):
							durum = "Senet Giriş(Alınan Senet)"
						if(sqlSenetler.Durum == "2"):
							durum = "Senet Çıkış(Cari Hesaba)"
						if(sqlSenetler.Durum == "3"):
							durum = "Senet Çıkış(Banka Tahsil)"
						if(sqlSenetler.Durum == "4"):
							durum = "Senet Çıkış(Banka Teminat)"
						if(sqlSenetler.Durum == "5"):
							durum = "Portföyde"
						context = {
							"ajaxBordroNo"     : sqlSenetler.BordroNo,
							"ajaxBordroTarihi" : sqlSenetler.BordroTarihi,
							"ajaxSenetNo"      : sqlSenetler.SenetNo,
							"ajaxTipi"         : tipi,
							"ajaxDurum"        : durum,
							"ajaxVade"         : sqlSenetler.Vade,
							"ajaxTutar"        : sqlSenetler.Tutar,
							"ajaxDoviz"        : doviz,
							"ajaxCariKodu"     : sqlSenetler.CariKodu,
							"ajaxOdemeYeri"    : sqlSenetler.OdemeYeri,
						}
						return JsonResponse(context)

					ajaxBordroIptal	= request.POST.get("ajaxBordroIptal")
					if(ajaxBordroIptal):
						sqlSenetIptal = get_object_or_404(Senet,id=ajaxBordroIptal)
						sqlSenetIptal.IsCanceled = True
						sqlSenetIptal.save()
						sqlSenetDurumGuncelle = get_object_or_404(Senet,SenetNo=sqlSenetIptal.SenetNo, Tipi="1", IsTransferCache=True)
						sqlSenetDurumGuncelle.Durum = "5"
						sqlSenetDurumGuncelle.IsTransferCache = False
						sqlSenetDurumGuncelle.save()
						context = {"ajaxMesaj": "İptal İşlemi Başarılı!",}
						return JsonResponse(context)	
					
					ajaxSenetNo   = request.POST.get("ajaxSenetNo")
					ajaxSenetTipi = request.POST.get("ajaxSenetTipi")
					if(ajaxSenetNo):
						try:
							sqlSenetDurum = get_object_or_404(Senet,SenetNo=ajaxSenetNo,Tipi=ajaxSenetTipi)
							sqlSenetDurum.IsTransferred = True
							sqlSenetDurum.OdemeAraciDurum = "5"
							sqlSenetDurum.save()
							context = {"ajaxMesaj": "1",}
							return JsonResponse(context)
						except:
							pass
				sqlAlinanSenetler  = Senet.objects.filter(Tipi=1,IsCanceled=False,Durum="5")
				sqlVerilenSenetler = Senet.objects.filter(Tipi=2,IsCanceled=False)
				context = {
					"modulYetkisi" 	     : modulYetkisi,
					"islemlerKontrol"    : islemlerKontrol,
					"sqlAlinanSenetler"  : sqlAlinanSenetler,
					"sqlVerilenSenetler" : sqlVerilenSenetler,
				}
				return render (request, "ceksenet/senetlerlistele.html", context)		
			else:		
				messages.success(request, "Senetler Listesini Görüntüleme Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")

def Tanimlamalar(request):
	try:
		kullaniciKontrol = get_object_or_404(Kullanicilar,KullaniciKodu=request.session['KullaniciKodu'],KullaniciDurumu=True)
		modulYetkisi = get_object_or_404(ModulYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
		if(modulYetkisi.IsCekSenet == True):
			islemlerKontrol = get_object_or_404(TanimlamaYetkileri,KullaniciTipiKodu=kullaniciKontrol.KullaniciTipi)
			if(islemlerKontrol.IsCekSenetTanimlamalari == True):
				ajaxBordroNo = request.POST.get("ajaxBordroNo")
				ajaxCekNo    = request.POST.get("ajaxCekNo")
				ajaxSenet    = request.POST.get("ajaxSenet")
				try:
					sqlOdemeAraciNo = get_object_or_404(OdemeAraciNoModel,id="1")
					if request.is_ajax():
						sqlOdemeAraciNo.BordroNo = ajaxBordroNo
						sqlOdemeAraciNo.CekNo    = ajaxCekNo
						sqlOdemeAraciNo.SenetNo  = ajaxSenet
						sqlOdemeAraciNo.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !",}
						return JsonResponse(context)
				except:
					if request.is_ajax():
						sqlOdemeAraciNoOlustur = OdemeAraciNoModel()
						sqlOdemeAraciNoOlustur.BordroNo = ajaxBordroNo
						sqlOdemeAraciNoOlustur.CekNo    = ajaxCekNo
						sqlOdemeAraciNoOlustur.SenetNo  = ajaxSenet
						sqlOdemeAraciNoOlustur.save()
						context = {"ajaxMesaj" : "Kayıt Başarılı !"}
						return JsonResponse(context)
					sqlOdemeAraciNo = ""				
				context = {
					"modulYetkisi" 	  : modulYetkisi,
					"sqlOdemeAraciNo" : sqlOdemeAraciNo,
				}		
				return render (request, "ceksenet/tanimlamalar.html", context)
			else:		
				messages.success(request, "Tanımlama Oluşturmaya Yetkiniz Yok !")
				return redirect("anasayfa:anasayfa")
		else:
			messages.success(request, "Bu Modüle Girmeye Yetkiniz Yok !")
			return redirect("kullanicilar:giris")
	except:
		messages.success(request, "Böyle Bir Kullanıcı Yok !")
		return redirect("kullanicilar:giris")		