import re
from django.template.response import TemplateResponse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from nav.models import UrlAlias
from nodes.models import Node
from lib.paginator import DrupalPaginator


def frontpage(request):
    lang_filter = Q(language='') | Q(language='en')
    articles = Node.objects.filter(promote=True).filter(lang_filter).order_by('-created')
    paginator = DrupalPaginator(articles, request=request)
    context = dict(page=paginator.page(), singlecolumn=True)
    return TemplateResponse(request, 'frontpage.jade', context)


def view_node(request, pk=None, lang=None, path=None):
    print 'request.path=%s pk=%s lang=%s path=%s' % (request.path, pk, lang, path)
    if not pk:
        kwargs = dict(dst=path)
        if lang:
            kwargs['language'] = lang
        alias = get_object_or_404(UrlAlias, **kwargs)
        mo = re.match('node/(\d+)', alias.src)
        if not mo:
            return HttpResponseServerError(_('Unexpected node url in database'))
        pk = int(mo.group(1))
    node = get_object_or_404(Node, pk=pk)
    url = node.get_absolute_url()
    if not path and url != request.path.lstrip('/'):
        return HttpResponseRedirect(url)
    return TemplateResponse(request, 'node.jade', dict(node=node))
