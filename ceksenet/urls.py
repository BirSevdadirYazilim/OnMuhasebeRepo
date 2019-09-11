from django.conf.urls import url
from .views import *

app_name = "ceksenet"

urlpatterns = [
    url(r'^cekbordro/$', CekBordroOlustur, name="cekbordro"),
    url(r'^senetbordro/$', SenetBordroOlustur, name="senetbordro"),
    url(r'^ceklerlistele/$', CeklerListele, name="ceklerlistele"),
    url(r'^senetlerlistele/$', SenetlerListele, name="senetlerlistele"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]