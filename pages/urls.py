from django.conf.urls import url
from django.template.response import TemplateResponse


urlpatterns = [
    url(r'^$', lambda request: TemplateResponse(request, 'index.jade')),
]
