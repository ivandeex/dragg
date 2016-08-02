from django.contrib import admin
from lib.admin import ReadonlyModelAdmin
from news import models


class FeedAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.Feed
    fields = ('fid', 'title', 'url', 'link', 'refresh', 'checked',
              'category_list', 'item_count')
    readonly_fields = fields
    list_display = ('fid', 'title', 'link', 'category_list', 'checked', 'item_count')
    list_filter = ('categories__title',)
    ordering = ('title',)


class ItemAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.Item
    list_display = ('iid', 'feed_title', 'title', 'link', 'timestamp')
    list_filter = ('feed__title', 'feed__categories__title')
    fields = list_display + ('category_list', 'description')
    readonly_fields = fields

    def feed_title(self, obj):
        return obj.feed.title


admin.site.register(models.Feed, FeedAdmin)
admin.site.register(models.Item, ItemAdmin)
