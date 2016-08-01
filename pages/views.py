from django.template.response import TemplateResponse
from django.db.models import Q
from pages.models import Node
from lib.paginator import DrupalPaginator


def frontpage(request):
    lang_filter = Q(language='') | Q(language='en')
    articles = Node.objects.filter(promote=True).filter(lang_filter).order_by('-created')
    paginator = DrupalPaginator(articles, request=request)
    context = dict(page=paginator.page(), singlecolumn=True)
    return TemplateResponse(request, 'frontpage.jade', context)
