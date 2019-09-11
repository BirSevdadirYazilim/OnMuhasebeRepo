from django.conf.urls import url
from .views import *

app_name = "stok"

urlpatterns = [
    url(r'^olustur/$', StokOlustur, name="olustur"),
    url(r'^listele/$', StokListele, name="listele"),
    url(r'^stokhareketleri/$', StokHareketleriListele, name="stokhareketleri"),
]


						