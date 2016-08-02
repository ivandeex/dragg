import re
from django.template.response import TemplateResponse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from nav.models import UrlAlias
from nodes.models import Node
from lib.paginator import DrupalPaginator
from lib.views import get_lang


def frontpage(request):
    lang = get_lang(request) or 'en'
    lang_filter = Q(language=lang) | Q(language='')
    nodes = Node.objects.filter(promote=True).filter(lang_filter).order_by('-created')
    paginator = DrupalPaginator(nodes, request=request)
    context = dict(page=paginator.page(), singlecolumn=True)
    return TemplateResponse(request, 'frontpage.jade', context)


def view_node(request, pk=None, path=None):
    lang = get_lang(request)
    print 'pk=%s path=%s lang="%s"' % (pk, path, lang)
    if not pk:
        if lang:
            alias = get_object_or_404(UrlAlias, dst=path, language=lang)
        else:
            alias = get_object_or_404(UrlAlias, dst=path)

        mo = re.match('node/(\d+)$', alias.src)
        if not mo:
            return HttpResponseServerError(_('Unexpected node url in database'))
        pk = int(mo.group(1))

    node = get_object_or_404(Node, pk=pk)
    url = node.get_absolute_url()
    if not path and url != request.path.lstrip('/'):
        # the node was requested as /[ru|en]/node/NNN
        return HttpResponseRedirect(url)

    return TemplateResponse(request, 'node.jade', dict(node=node))
