from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.static import serve
from nodes import views as node_views

common_patterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', node_views.frontpage),
    url(r'^node/(?P<pk>\d+)(?:/.*)?$', node_views.view_node),
    url(r'^(?P<path>(book|page|story)/.+)$', node_views.view_node),
    url(r'^sites/(?P<path>.*)$', serve, {'document_root': settings.SITES_ROOT}),
]

static_regex = r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/')
static_pattern = url(static_regex, serve, {'document_root': settings.STATIC_ROOT})

urlpatterns = common_patterns + i18n_patterns(*common_patterns) + [static_pattern]
