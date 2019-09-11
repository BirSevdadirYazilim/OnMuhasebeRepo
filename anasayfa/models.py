from django.db import models

class Duyurular(models.Model):
	DuyuruKodu     = models.CharField(max_length=10)
	Baslik         = models.CharField(max_length=50)
	Icerik         = models.TextField()
	KullaniciGrubu = models.CharField(max_length=10,null=True)
	Kullanici      = models.CharField(max_length=10)
	Durumu         = models.IntegerField()

class Gorevler(models.Model):
	GorevKodu      = models.CharField(max_length=10)
	Baslik         = models.CharField(max_length=50)
	Icerik         = models.TextField()
	KullaniciGrubu = models.CharField(max_length=10,null=True)
	Kullanici      = models.CharField(max_length=10)
	Durumu         = models.IntegerField()

class Hatirlatmalar(models.Model):
	HatirlatmaKodu = models.CharField(max_length=10)
	Baslik 		   = models.CharField(max_length=50)
	Icerik 		   = models.TextField()
	KullaniciGrubu = models.CharField(max_length=10,null=True)
	Kullanici      = models.CharField(max_length=10)
	Durumu         = models.IntegerField()

