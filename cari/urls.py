from django.conf.urls import url
from .views import *

app_name = "cari"

urlpatterns = [
    url(r'^olustur/$', CariOlustur, name="olustur"),
    url(r'^listele/$', CariListele, name="listele"),
    url(r'^carihareketleri/$', CariHareketleri, name="carihareketleri"),
]