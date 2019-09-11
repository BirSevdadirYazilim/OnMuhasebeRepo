from django.conf.urls import url
from .views import *

app_name = "anasayfa"

urlpatterns = [
	url(r'^$', AnasayfaView, name="anasayfa"),
    url(r'^islemlerim/$', KullaniciIslemlerim, name="islemlerim"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]