from django.db import models
from django.urls import reverse

class Kullanicilar(models.Model):
	KullaniciKodu 	 = models.CharField(max_length=10)
	KullaniciAdi 	 = models.CharField(max_length=50)
	KullaniciParola  = models.CharField(max_length=100)
	KullaniciTipi    = models.CharField(max_length=50)
	KullaniciGrubu   = models.CharField(max_length=50, null=True)
	KullaniciDurumu	 = models.BooleanField(default=False)
	SonGiris 		 = models.DateTimeField(null=True)
	KayitTarihi 	 = models.DateTimeField(null=True)
	KayitYapan		 = models.CharField(max_length=50,null=True)
	DuzeltmeTarihi 	 = models.DateTimeField(null=True)
	DuzeltmeYapan	 = models.CharField(max_length=50,null=True)
	IsSaved 		 = models.BooleanField(default=False)
	IsVerified		 = models.BooleanField(default=False)
	IsDeleted		 = models.BooleanField(default=False)
	IsCanceled       = models.BooleanField(default=False)
	IsTransferred	 = models.BooleanField(default=False)
	IsTransferCache	 = models.BooleanField(default=False)

	def __str__(self):
		return self.KullaniciKodu

class KullaniciTipiModel(models.Model):
	KullaniciTipiKodu  = models.CharField(max_length=10)
	KullaniciTipi      = models.CharField(max_length=50)

class KullaniciGrubuModel(models.Model):
	KullaniciGrubuKodu = models.CharField(max_length=10)
	KullaniciGrubu     = models.CharField(max_length=50)	

class ModulYetkileri(models.Model):
	KullaniciTipiKodu  = models.CharField(max_length=10)
	IsAnaSayfa	       = models.BooleanField(default=True)
	IsCari		       = models.BooleanField(default=False)
	IsKasa		       = models.BooleanField(default=False)
	IsBanka	           = models.BooleanField(default=False)
	IsCekSenet	       = models.BooleanField(default=False)
	IsSiparis          = models.BooleanField(default=False)
	IsFatura           = models.BooleanField(default=False)
	IsIrsaliye         = models.BooleanField(default=False)
	IsStok 		       = models.BooleanField(default=False)
	IsKullanicilar     = models.BooleanField(default=False)
	IsTanimlamalar     = models.BooleanField(default=False)

class KullaniciYetkileri(models.Model):
	KullaniciTipiKodu 	= models.CharField(max_length=10)
	IsKullaniciOlustur  = models.BooleanField(default=False)
	IsKullaniciListele  = models.BooleanField(default=False)
	IsKullaniciDetay    = models.BooleanField(default=False)
	IsKullaniciGuncelle = models.BooleanField(default=False)
	IsKullaniciSil      = models.BooleanField(default=False)


class KasaYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsKasaOlustur     = models.BooleanField(default=False)
	IsKasaListele     = models.BooleanField(default=False)
	IsKasaDetay       = models.BooleanField(default=False)
	IsKasaGuncelle    = models.BooleanField(default=False)
	IsKasaSil         = models.BooleanField(default=False)

class KasaHareketleriYetkileri(models.Model):
	KullaniciTipiKodu 	     = models.CharField(max_length=10)
	IsKasaHareketleriOlustur = models.BooleanField(default=False)
	IsKasaHareketleriListele = models.BooleanField(default=False)
	IsKasaHareketleriDetay   = models.BooleanField(default=False)
	IsKasaHareketleriIptalEt = models.BooleanField(default=False)
	IsKasaHareketleriSil     = models.BooleanField(default=False)

class BankaYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsBankaOlustur    = models.BooleanField(default=False)
	IsBankaListele    = models.BooleanField(default=False)
	IsBankaDetay      = models.BooleanField(default=False)
	IsBankaGuncelle   = models.BooleanField(default=False)
	IsBankaSil        = models.BooleanField(default=False)	

class BankaHareketleriYetkileri(models.Model):
	KullaniciTipiKodu 	 	  = models.CharField(max_length=10)
	IsBankaHareketleriOlustur = models.BooleanField(default=False)
	IsBankaHareketleriListele = models.BooleanField(default=False)
	IsBankaHareketleriDetay   = models.BooleanField(default=False)
	IsBankaHareketleriIptalEt = models.BooleanField(default=False)
	IsBankaHareketleriSil     = models.BooleanField(default=False)

class CariYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsCariOlustur     = models.BooleanField(default=False)
	IsCariListele     = models.BooleanField(default=False)
	IsCariDetay       = models.BooleanField(default=False)
	IsCariGuncelle    = models.BooleanField(default=False)
	IsCariSil         = models.BooleanField(default=False)

class CariHareketleriYetkileri(models.Model):
	KullaniciTipiKodu        = models.CharField(max_length=10)
	IsCariHareketleriListele = models.BooleanField(default=False)
	IsCariHareketleriDetay   = models.BooleanField(default=False)	

class CekSenetYetkileri(models.Model):
	KullaniciTipiKodu    = models.CharField(max_length=10)
	IsCekBordroOlustur   = models.BooleanField(default=False)
	IsCekListele         = models.BooleanField(default=False)
	IsCekDetay           = models.BooleanField(default=False)
	IsCekIslemler        = models.BooleanField(default=False)
	IsCekIptalEt         = models.BooleanField(default=False)
	IsCekSil             = models.BooleanField(default=False)
	IsSenetBordroOlustur = models.BooleanField(default=False)
	IsSenetListele       = models.BooleanField(default=False)
	IsSenetDetay         = models.BooleanField(default=False)
	IsSenetIslemler      = models.BooleanField(default=False)
	IsSenetIptalEt       = models.BooleanField(default=False)
	IsSenetSil           = models.BooleanField(default=False)
	
class FaturaYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsFaturaOlustur   = models.BooleanField(default=False)
	IsFaturaListele   = models.BooleanField(default=False)
	IsFaturaDetay     = models.BooleanField(default=False)
	IsFaturaIptalEt   = models.BooleanField(default=False)
	IsFaturaIrsaliye  = models.BooleanField(default=False)
	IsFaturaSil       = models.BooleanField(default=False)	

class IrsaliyeYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsIrsaliyeOlustur = models.BooleanField(default=False)
	IsIrsaliyeListele = models.BooleanField(default=False)
	IsIrsaliyeDetay   = models.BooleanField(default=False)
	IsIrsaliyeIptalEt = models.BooleanField(default=False)
	IsIrsaliyeFatura  = models.BooleanField(default=False)
	IsIrsaliyeSil     = models.BooleanField(default=False)

class SiparisYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsSiparisOlustur  = models.BooleanField(default=False)
	IsSiparisListele  = models.BooleanField(default=False)
	IsSiparisDetay    = models.BooleanField(default=False)
	IsSiparisIptalEt  = models.BooleanField(default=False)
	IsSiparisFatura   = models.BooleanField(default=False)
	IsSiparisSil      = models.BooleanField(default=False)


class StokYetkileri(models.Model):
	KullaniciTipiKodu = models.CharField(max_length=10)
	IsStokOlustur     = models.BooleanField(default=False)
	IsStokListele     = models.BooleanField(default=False)
	IsStokDetay       = models.BooleanField(default=False)
	IsStokGuncelle    = models.BooleanField(default=False)
	IsStokSil         = models.BooleanField(default=False)	

class StokHareketleriYetkileri(models.Model):
	KullaniciTipiKodu 	 	 = models.CharField(max_length=10)
	IsStokHareketleriListele = models.BooleanField(default=False)
	IsStokHareketleriDetay   = models.BooleanField(default=False)

class TanimlamaYetkileri(models.Model):
	KullaniciTipiKodu 	     = models.CharField(max_length=10)
	IsAnasayfaTanimlamalari  = models.BooleanField(default=False)
	IsKasaTanimlamalari      = models.BooleanField(default=False)
	IsBankaTanimlamalari     = models.BooleanField(default=False)
	IsCekSenetTanimlamalari  = models.BooleanField(default=False)
	IsSiparisTanimlamalari   = models.BooleanField(default=False)
	IsFaturaTanimlamalari    = models.BooleanField(default=False)
	IsIrsaliyeTanimlamalari  = models.BooleanField(default=False)
	IsKullaniciTanimlamalari = models.BooleanField(default=False)	