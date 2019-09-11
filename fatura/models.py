from django.db import models
from django.urls import reverse

class Fatura(models.Model):
	CariKodu	    = models.CharField(max_length=10)
	KullaniciKodu   = models.CharField(max_length=10)
	FaturaSeri		= models.CharField(max_length=10)
	FaturaSira		= models.IntegerField()
	FaturaTipi		= models.CharField(max_length=10)
	IslemTarihi	    = models.DateField()
	ToplamBrutTutar = models.DecimalField(max_digits=10,decimal_places=2)
	ToplamKdv       = models.DecimalField(max_digits=10,decimal_places=2)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified	    = models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)
   
	def __str__(self):
		return self.FaturaSira	
    	
class FaturaHareketleri(models.Model):
	FaturaSeri		= models.CharField(max_length=10)
	FaturaSira		= models.IntegerField()
	StokKodu        = models.CharField(max_length=10)
	Miktar          = models.IntegerField()
	Nitelik         = models.CharField(max_length=10)
	BirimFiyat      = models.DecimalField(max_digits=10,decimal_places=2)
	IskontoOrani    = models.IntegerField(null=True,blank=True,default=0)
	KdvOrani 		= models.IntegerField()
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache = models.BooleanField(default=False)

	def __str__(self):
		return self.FaturaSira

class FaturaNo(models.Model):
	FaturaSeri = models.CharField(max_length=10)
	FaturaSira = models.IntegerField()		