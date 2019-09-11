from django.db import models
from django.urls import reverse

class Stok(models.Model):
	StokKodu		    = models.CharField(max_length=10)
	StokAdi             = models.CharField(max_length=100)
	StokNitelik         = models.CharField(max_length=10)
	StokMiktar          = models.IntegerField()
	AlisFiyati 	        = models.DecimalField(max_digits=10,decimal_places=2, null=True)
	SatisFiyati 	    = models.DecimalField(max_digits=10,decimal_places=2, null=True)
	KdvOrani            = models.IntegerField()
	StokKaydiOlusturan  = models.CharField(max_length=50)
	StokKayitTarihi	    = models.DateTimeField()
	StokKaydiDuzenleyen = models.CharField(null=True,max_length=50)
	StokDuzenlemeTarihi = models.DateTimeField(null=True)
	IsSaved 		    = models.BooleanField(default=False)
	IsVerified		    = models.BooleanField(default=False)
	IsDeleted		    = models.BooleanField(default=False)
	IsCanceled     	    = models.BooleanField(default=False)
	IsTransferred	    = models.BooleanField(default=False)
	IsTransferCache	    = models.BooleanField(default=False)

	def __str__(self):
 		return self.StokKodu

class StokHareketleri(models.Model):
	StokKodu		      = models.CharField(max_length=10)
	StokAdi               = models.CharField(max_length=100)
	StokNitelik           = models.CharField(max_length=10)
	StokMiktar            = models.IntegerField()
	AlisFiyati 	          = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	SatisFiyati 	      = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	SonIskontoOrani       = models.IntegerField(null=True,blank=True)
	StokHareketiOlusturan = models.CharField(max_length=50)
	StokHareketTarihi     = models.DateTimeField()
	IsSaved 		      = models.BooleanField(default=False)
	IsVerified		      = models.BooleanField(default=False)
	IsDeleted		      = models.BooleanField(default=False)
	IsCanceled     	      = models.BooleanField(default=False)
	IsTransferred	      = models.BooleanField(default=False)
	IsTransferCache	      = models.BooleanField(default=False)

	def __str__(self):
 		return self.StokKodu	