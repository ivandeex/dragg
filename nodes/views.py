import re
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from nav.models import UrlAlias
from nodes.models import Node
from lib.views import get_lang


def node_path_view(request, path):
    lang = get_lang('')
    if lang:
        alias = get_object_or_404(UrlAlias, dst=path, language=lang)
    else:
        alias = get_object_or_404(UrlAlias, dst=path)
    pk = int(re.match('node/(\d+)$', alias.src).group(1))
    return node_pk_view(request, pk, redirect=False)


def node_pk_view(request, pk, redirect=True):
    node = get_object_or_404(Node, pk=pk)
    if redirect:
        return HttpResponseRedirect(node.get_absolute_url())
    return TemplateResponse(request, 'node.jade', dict(node=node))
