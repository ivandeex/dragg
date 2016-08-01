from django.template.response import TemplateResponse
from django.db.models import Q
from pages.models import Node


def frontpage(request):
    lang_filter = Q(language='') | Q(language='en')
    articles = Node.objects.filter(promote=True).filter(lang_filter)
    page_size = 10
    context = {
        'articles': articles.order_by('-created')[:page_size]
    }
    return TemplateResponse(request, 'frontpage.jade', context)
