from django.db import models
from django.urls import reverse

class Cari(models.Model):
	CariKodu        = models.CharField(max_length=10)
	CariUnvani      = models.CharField(max_length=150)
	VergiDairesi    = models.CharField(max_length=50)	
	VergiNumarasi   = models.IntegerField()
	IsSaved 	    = models.BooleanField(default=False)
	IsVerified	    = models.BooleanField(default=False)
	IsDeleted	    = models.BooleanField(default=False)
	IsCanceled      = models.BooleanField(default=False)
	IsTransferred   = models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)

	def __str__(self):
		return self.CariKodu

class CariIrtibat(models.Model):
	CariKodu     	= models.CharField(max_length=10)
	Il           	= models.CharField(max_length=50)
	Ilce         	= models.CharField(max_length=50)
	Adres        	= models.CharField(max_length=150)
	PostaKodu    	= models.IntegerField()
	KEP			 	= models.EmailField(null=True)
	Tel1         	= models.CharField(max_length=15)
	Tel2         	= models.CharField(max_length=15, null=True)
	Email        	= models.EmailField(null=True)
	WebSitesi    	= models.CharField(max_length=50, null=True)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)

	def __str__(self):
		return self.CariKodu

class CariLokasyon(models.Model):
	CariKodu        = models.CharField(max_length=10)
	LokasyonKodu    = models.CharField(max_length=10,null=True)
	LokasyonDetay   = models.CharField(max_length=100,null=True)
	IsSaved 	    = models.BooleanField(default=False)
	IsVerified	    = models.BooleanField(default=False)
	IsDeleted	    = models.BooleanField(default=False)
	IsCanceled      = models.BooleanField(default=False)
	IsTransferred   = models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)	

	def __str__(self):
		return self.LokasyonKodu