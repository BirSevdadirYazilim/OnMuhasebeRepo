from django.conf.urls import url
from .views import *

app_name = "kasa"

urlpatterns = [
    url(r'^olustur/$', KasaOlustur, name="olustur"),
    url(r'^listele/$', KasaListele, name="listele"),
    url(r'^hareketler/$', KasaHareketleriListele, name="hareketler"),
    url(r'^giris-cikis/$', KasaHareketleriOlustur, name="giris-cikis"),
    url(r'^transfer/$', HesaplarArasiTransfer, name="transfer"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]