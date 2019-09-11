from django.conf.urls import url
from .views import *

app_name = "kullanicilar"

urlpatterns = [
    url(r'^listele/$', KullaniciListele, name="listele"),
    url(r'^giris/$', KullaniciGiris, name="giris"),
    url(r'^kayit/$', KullaniciKayit, name="kayit"),
    url(r'^cikis/$', KullaniciCikis, name="cikis"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]
