import re
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from lib.paginator import DrupalPaginator
from nodes.models import Node
from nav.models import Term, UrlAlias
from lib.views import get_lang


def frontpage(request):
    lang = get_lang('en')
    lang_filter = Q(language=lang) | Q(language='')
    nodes = Node.objects.filter(promote=True).filter(lang_filter).order_by('-created')
    paginator = DrupalPaginator(nodes, request=request)
    context = dict(page=paginator.page(), singlecolumn=True)
    return TemplateResponse(request, 'frontpage.jade', context)


def term_name_view(request, name):
    path = 'tag/' + name
    lang = get_lang('')
    if lang:
        alias = get_object_or_404(UrlAlias, dst=path, language=lang)
    else:
        alias = get_object_or_404(UrlAlias, dst=path)
    pk = int(re.match('taxonomy/term/(\d+)$', alias.src).group(1))
    return term_pk_view(request, pk, redirect=False)


def term_pk_view(request, pk, redirect=True):
    term = get_object_or_404(Term, pk=pk)
    if redirect:
        return HttpResponseRedirect(term.get_absolute_url())

    lang = get_lang('en')
    lang_filter = Q(language=lang) | Q(language='')

    nodes = Node.objects.filter(terms=term)
    nodes = nodes.filter(lang_filter).order_by('-created')
    page = DrupalPaginator(nodes, request=request).page()

    singlecolumn = term.name in ('projects', 'library')
    return TemplateResponse(request, 'termpage.jade',
                            dict(page_term=term, page=page, singlecolumn=singlecolumn))
