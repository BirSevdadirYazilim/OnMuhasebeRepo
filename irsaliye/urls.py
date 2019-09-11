from django.conf.urls import url
from .views import *
app_name = "irsaliye"

urlpatterns = [
    url(r'^olustur/$', IrsaliyeOlustur, name="olustur"),
    url(r'^listele/$', IrsaliyeListele, name="listele"),
    url(r'^tanimlamalar/$', Tanimlamalar, name="tanimlamalar"),
]