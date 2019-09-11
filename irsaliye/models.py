from django.db import models
from django.urls import reverse

class Irsaliye(models.Model):
	IrsaliyeNo       = models.CharField(max_length=10)
	IrsaliyeTipi     = models.CharField(max_length=10)
	DuzenlenmeTarihi = models.DateField()
	DuzenlenmeSaati  = models.TimeField()
	SevkTarihi       = models.DateField()
	SevkSaati        = models.TimeField()
	TeslimEden       = models.CharField(max_length=30)
	TeslimAlan       = models.CharField(max_length=30)
	TeslimSaati      = models.TimeField()
	CariKodu		 = models.CharField(max_length=10)
	KullaniciKodu	 = models.CharField(max_length=10)
	ToplamBrutTutar  = models.DecimalField(max_digits=10,decimal_places=2)
	ToplamKdv        = models.DecimalField(max_digits=10,decimal_places=2)
	IsSaved 		 = models.BooleanField(default=False)
	IsVerified		 = models.BooleanField(default=False)
	IsDeleted		 = models.BooleanField(default=False)
	IsCanceled     	 = models.BooleanField(default=False)
	IsTransferred	 = models.BooleanField(default=False)
	IsTransferCache	 = models.BooleanField(default=False)
   
	def __str__(self):
		return self.IrsaliyeNo	
    	
class IrsaliyeHareketleri(models.Model):
	IrsaliyeNo      = models.CharField(max_length=10)
	IrsaliyeTipi	= models.CharField(max_length=10)
	SevkTarihi      = models.DateField()
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
		return self.IrsaliyeNo

class IrsaliyeNo(models.Model):
	SatisIrsaliyesiNo = models.CharField(max_length=10)
