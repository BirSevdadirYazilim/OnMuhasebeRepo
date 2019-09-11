from django.conf.urls import url
from .views import *

app_name = "banka"

urlpatterns = [
    url(r'^olustur/$', BankaOlustur, name="olustur"),
    url(r'^listele/$', BankaListele, name="listele"),
    url(r'^giris-cikis/$', BankaHareketleriOlustur, name="giris-cikis"),
    url(r'^hareketler/$', BankaHareketleriListele, name="hareketler"),
    url(r'^transfer/$', HesaplarArasiTransfer, name="transfer"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]