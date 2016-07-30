from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models


class ReadonlyModelAdmin(object):
    list_per_page = 50
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class NodeRevInline(ReadonlyModelAdmin, admin.StackedInline):
    model = models.NodeRev
    fields = ('vid', 'title', 'timestamp', 'format_name', 'teaser', 'body')
    readonly_fields = fields
    max_num = 0

    def format_name(self, obj):
        return obj.format.name


class NodeAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.Node
    list_display = ('nid', 'type_id', 'language', 'title', 'created', 'changed', 'promote')
    list_filter = ('type_id', 'language', 'promote')
    ordering = ('-created',)
    search_fields = ('title', 'rev__body', 'rev__teaser')
    fields = ('nid', 'type_id', 'language', 'title', 'status', 'created', 'changed',
              'term_line', 'story_url', 'url', 'promote', 'sticky')
    readonly_fields = fields
    inlines = (NodeRevInline,)

    def term_line(self, obj):
        return ', '.join(sorted(set(t.name for t in obj.terms.all())))
    term_line.short_description = _('Node terms')

    def story_url(self, obj):
        return obj.story_url() or '-'
    story_url.short_description = _('Story URL')


class UrlAliasAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.UrlAlias
    fields = ('src', 'dst', 'language')
    list_display = fields
    list_filter = ('language',)
    readonly_fields = fields
    search_fields = ('dst',)
    ordering = ('src',)


class FilterAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.Filter
    fields = ('fid', 'format_name', 'delta', 'weight')
    readonly_fields = fields
    list_display = fields
    list_filter = ('format__name',)
    ordering = ('format_id', 'weight')

    def format_name(self, obj):
        return obj.format.name


class NewsFeedAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.NewsFeed
    fields = ('fid', 'title', 'url', 'link', 'refresh', 'checked',
              'category_list', 'item_count')
    readonly_fields = fields
    list_display = ('fid', 'title', 'link', 'category_list', 'checked', 'item_count')
    list_filter = ('categories__title',)
    ordering = ('title',)


class NewsItemAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.NewsItem
    list_display = ('iid', 'feed_title', 'title', 'link', 'timestamp')
    list_filter = ('feed__title', 'feed__categories__title')
    fields = list_display + ('category_list', 'description')
    readonly_fields = fields
    ordering = ('-timestamp',)

    def feed_title(self, obj):
        return obj.feed.title


admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.UrlAlias, UrlAliasAdmin)
admin.site.register(models.Filter, FilterAdmin)
admin.site.register(models.NewsFeed, NewsFeedAdmin)
admin.site.register(models.NewsItem, NewsItemAdmin)
