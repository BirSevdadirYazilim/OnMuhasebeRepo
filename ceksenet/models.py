from django.db import models
from django.urls import reverse

class Cek(models.Model):
	BordroNo        = models.CharField(max_length=10)
	BordroTarihi    = models.DateField()  
	CekNo           = models.CharField(max_length=10)
	Tipi            = models.CharField(max_length=1)
	Durum           = models.CharField(max_length=1)
	Vade            = models.DateField()
	Tutar           = models.DecimalField(max_digits=10,decimal_places=2)
	Doviz           = models.CharField(max_length=10)
	CariKodu        = models.CharField(max_length=10)
	BankaAdi        = models.CharField(max_length=50)
	SubeKodu        = models.CharField(max_length=50)
	HesapNo         = models.IntegerField()
	OdemeYeri       = models.CharField(max_length=100)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache = models.BooleanField(default=False)

	def __str__(self):
			return self.CekNo

class Senet(models.Model):
	BordroNo        = models.CharField(max_length=10)
	BordroTarihi    = models.DateField()  
	SenetNo         = models.CharField(max_length=10)
	Tipi            = models.CharField(max_length=1)
	Durum           = models.CharField(max_length=1)
	Vade            = models.DateField()
	Tutar           = models.DecimalField(max_digits=10,decimal_places=2)
	Doviz           = models.CharField(max_length=10)
	CariKodu        = models.CharField(max_length=10)
	OdemeYeri       = models.CharField(max_length=50)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache = models.BooleanField(default=False)

	def __str__(self):
 		return self.SenetNo				

class OdemeAraciNoModel(models.Model):
	BordroNo = models.CharField(max_length=10, null=True)
	CekNo    = models.CharField(max_length=10, null=True)
	SenetNo  = models.CharField(max_length=10, null=True)	