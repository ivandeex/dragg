from django.conf.urls import url
from nodes.views import frontpage, view_node


urlpatterns = [
    url(r'^$', frontpage),
    url(r'^(?:(?:en|ru)/)?node/(?P<pk>\d+)(?:/.*)?$', view_node),
    url(r'^(?:(?P<lang>en|ru)/)?(?P<path>(?:book|page|story)/.+)$', view_node),
]
