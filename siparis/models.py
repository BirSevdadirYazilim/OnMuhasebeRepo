from django.db import models
from django.urls import reverse

class Siparis(models.Model):
	CariKodu		= models.CharField(max_length=10)
	KullaniciKodu	= models.CharField(max_length=10)
	SiparisFisiNo	= models.CharField(max_length=10)
	SiparisTipi		= models.CharField(max_length=10)
	SiparisTarihi	= models.DateField()
	ToplamBrutTutar = models.DecimalField(max_digits=10,decimal_places=2)
	ToplamKdv       = models.DecimalField(max_digits=10,decimal_places=2)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)
   
	def __str__(self):
		return self.SiparisFisiNo	
    	
class SiparisHareketleri(models.Model):
	SiparisFisiNo   = models.CharField(max_length=10)
	SiparisTipi		= models.CharField(max_length=10)
	StokKodu        = models.CharField(max_length=10)
	SiparisTarihi	= models.DateField()
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
		return self.SiparisFisiNo

class SiparisFisiNo(models.Model):
	AlınanSiparisFisiNo  = models.CharField(max_length=10)
	VerilenSiparisFisiNo = models.CharField(max_length=10)	