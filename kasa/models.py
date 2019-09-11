from django.db import models
from django.urls import reverse

class Kasa(models.Model):
	KasaKodu            = models.CharField(max_length=10)
	KasaAdi             = models.CharField(max_length=50)
	KasaAcilisBakiyesi  = models.DecimalField(max_digits=10,decimal_places=2)
	KasaBorc		    = models.DecimalField(max_digits=10,decimal_places=2, null=True)
	KasaAlacak		    = models.DecimalField(max_digits=10,decimal_places=2, null=True)
	KasaAcilisTarihi    = models.DateField()
	KasaKaydiOlusturan  = models.CharField(max_length=50, null=True)
	KasaDuzenlemeTarihi = models.DateField(null=True)
	KasaKaydıDuzenleyen = models.CharField(max_length=50, null=True)
	Aciklama            = models.CharField(max_length=250, null=True)
	IsSaved 		    = models.BooleanField(default=False)
	IsVerified		    = models.BooleanField(default=False)
	IsDeleted		    = models.BooleanField(default=False)
	IsCanceled     	    = models.BooleanField(default=False)
	IsTransferred	    = models.BooleanField(default=False)
	IsTransferCache	    = models.BooleanField(default=False)

	def __str__(self):
		return self.KasaKodu

class KasaHareketleri(models.Model):
	KasaKodu        = models.CharField(max_length=10)
	KasaBorc		= models.DecimalField(max_digits=10,decimal_places=2, null=True)
	KasaAlacak		= models.DecimalField(max_digits=10,decimal_places=2, null=True)
	Makbuz          = models.CharField(max_length=50)
	MakbuzNo        = models.CharField(max_length=10)
	MakbuzTarihi    = models.DateField()
	Aciklama        = models.CharField(max_length=250, null=True)
	CariKodu        = models.CharField(max_length=10)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)

	def __str__(self):
		return self.KasaKodu

class MakbuzNo(models.Model):
	KasaKodu          = models.CharField(max_length=10)
	TahsilatMakbuzuNo = models.CharField(max_length=10,null=True)
	TediyeMakbuzuNo   = models.CharField(max_length=10,null=True)