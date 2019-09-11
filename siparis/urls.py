from django.conf.urls import url
from .views import *
app_name = "siparis"

urlpatterns = [
    url(r'^olustur/$', SiparisOlustur, name="olustur"),
    url(r'^listele/$', SiparisListele, name="listele"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]