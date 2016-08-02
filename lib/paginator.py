import urlparse
from django.conf import settings
from django.core.paginator import Page, Paginator


class DrupalPage(Page):
    def _build_url(self, number):
        request = self.paginator.request
        query = request.GET.copy()
        param = settings.PAGINATOR_QUERY
        if number > 1:
            query[param] = number - 1
        elif param in query:
            query.pop(param)
        return urlparse.urlunsplit((None, None, request.path, query.urlencode(), None))

    def first_url(self):
        return self._build_url(1)

    def prev_url(self):
        return self._build_url(self.number - 1)

    def next_url(self):
        return self._build_url(self.number + 1)

    def last_url(self):
        return self._build_url(self.paginator.num_pages)

    def _pager_start(self):
        num_pages = self.paginator.num_pages
        num_items = settings.PAGINATOR_ITEMS
        return 1 if num_pages < num_items else max(1, self.number - num_items // 2)

    def _pager_end(self):
        return min(self.paginator.num_pages + 1, self._pager_start() + settings.PAGINATOR_ITEMS)

    def pager_items(self):
        for number in range(self._pager_start(), self._pager_end()):
            yield self._build_url(number), str(number), number == self.number

    def pager_has_previous(self):
        return self._pager_start() > 1

    def pager_has_next(self):
        return self._pager_end() < self.paginator.num_pages


class DrupalPaginator(Paginator):

    def __init__(self, object_list, per_page=None, request=None, *args, **kwargs):
        self.request = request
        per_page = per_page or settings.PAGINATOR_SIZE
        super(DrupalPaginator, self).__init__(object_list, per_page, *args, **kwargs)

    def _get_page(self, *args, **kwargs):
        return DrupalPage(*args, **kwargs)

    def page(self, number=None):
        if number is None:
            try:
                number = int(self.request.GET[settings.PAGINATOR_QUERY])
            except Exception:
                number = 0
            number = min(self.num_pages, max(1, number + 1))
        return super(DrupalPaginator, self).page(number)
