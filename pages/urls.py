from django.conf.urls import url
from pages.views import frontpage


urlpatterns = [
    url(r'^$', frontpage),
]
