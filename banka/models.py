from django.db import models

class Banka(models.Model):
	BankaKodu            = models.CharField(max_length=10)
	BankaAdi             = models.CharField(max_length=50)
	BankaSube            = models.CharField(max_length=10)
	BankaIl              = models.CharField(max_length=50)
	BankaIlce            = models.CharField(max_length=50)
	BankaAcilisBakiyesi  = models.DecimalField(max_digits=10,decimal_places=2)
	BankaBorc		     = models.DecimalField(max_digits=10,decimal_places=2, null=True)
	BankaAlacak		     = models.DecimalField(max_digits=10,decimal_places=2, null=True)
	BankaAdres           = models.CharField(max_length=100)
	BankaTel1 	         = models.CharField(max_length=15)
	BankaTel2            = models.CharField(max_length=15, null=True)
	BankaHesapNo         = models.IntegerField()
	BankaIbanNo          = models.CharField(max_length=50)
	BankaYetkilisi       = models.CharField(max_length=100, null=True)
	BankaAcilisTarihi    = models.DateTimeField()
	BankaKaydiOlusturan  = models.CharField(max_length=50, null=True)
	BankaDuzenlemeTarihi = models.DateTimeField(null=True)
	BankaKaydıDuzenleyen = models.CharField(max_length=50, null=True)
	IsSaved 		     = models.BooleanField(default=False)
	IsVerified		     = models.BooleanField(default=False)
	IsDeleted		     = models.BooleanField(default=False)
	IsCanceled     	     = models.BooleanField(default=False)
	IsTransferred	     = models.BooleanField(default=False)
	IsTransferCache	     = models.BooleanField(default=False)

	def __str__(self):
 		return self.BankaKodu 	

class BankaHareketleri(models.Model):
	BankaKodu    	= models.CharField(max_length=10)
	BankaBorc		= models.DecimalField(max_digits=10,decimal_places=2, null=True)
	BankaAlacak		= models.DecimalField(max_digits=10,decimal_places=2, null=True)
	Dekont       	= models.CharField(max_length=50)
	DekontNo     	= models.CharField(max_length=10)
	DekontTarihi 	= models.DateField()
	Aciklama     	= models.CharField(max_length=250 ,null=True)
	CariKodu        = models.CharField(max_length=10)
	IsSaved 		= models.BooleanField(default=False)
	IsVerified		= models.BooleanField(default=False)
	IsDeleted		= models.BooleanField(default=False)
	IsCanceled     	= models.BooleanField(default=False)
	IsTransferred	= models.BooleanField(default=False)
	IsTransferCache	= models.BooleanField(default=False)

	def __str__(self):
		return self.BankaKodu

class DekontNo(models.Model):
	BankaKodu         = models.CharField(max_length=10)
	TahsilatDekontuNo = models.CharField(max_length=10,null=True)
	TediyeDekontuNo   = models.CharField(max_length=10,null=True)