from django.conf.urls import url
from .views import *

app_name = "fatura"

urlpatterns = [
    url(r'^olustur/$', FaturaOlustur, name="olustur"),
    url(r'^listele/$', FaturaListele, name="listele"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]