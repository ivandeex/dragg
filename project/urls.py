from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.static import serve
from nav import views as nav_views
from nodes import views as node_views

common_patterns = [
    url(r'^sites/(?P<path>.*)$', serve, {'document_root': settings.SITES_ROOT}),
    url(r'^(?P<path>(book|page|story)/.+)$', node_views.node_path_view),
    url(r'^node/(?P<pk>\d+)(?:/.*)?$', node_views.node_pk_view),
    url(r'^taxonomy/term/(?P<pk>\d+)$', nav_views.term_pk_view),
    url(r'^tag/(?P<name>[^/]+)$', nav_views.term_name_view),
    url(r'^$', nav_views.frontpage),
    url(r'^admin/', admin.site.urls),
]

static_regex = r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/')
static_pattern = url(static_regex, serve, {'document_root': settings.STATIC_ROOT})

urlpatterns = common_patterns + i18n_patterns(*common_patterns) + [static_pattern]
