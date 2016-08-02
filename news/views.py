from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from news.models import Category, Item
from lib.paginator import DrupalPaginator


def category_view(request, cid=None):
    news_title = 'News'
    if cid == 'all':
        cat = None
        title = 'Feed aggregator'
    elif cid == 'news':
        title = news_title
        cat = get_object_or_404(Category, title=title)
    else:
        cat = get_object_or_404(Category, cid=int(cid))
        title = cat.title
        if title == news_title:
            return HttpResponseRedirect('/news')
    if cat:
        items = Item.objects.filter(feed__categories=cat)
    else:
        items = Item.objects.all()
    page = DrupalPaginator(items.order_by('-timestamp'), request=request).page()
    return TemplateResponse(request, 'category_view.jade',
                            dict(page=page, title=title, singlecolumn=True))


def category_list_view(request):
    return TemplateResponse(request, 'category_list.jade',
                            dict(categories=Category.objects.order_by('title'),
                                 singlecolumn=True))
