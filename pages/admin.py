from django.contrib import admin
from lib.admin import ReadonlyModelAdmin
from pages import models


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


class FilterAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.Filter
    fields = ('fid', 'format_name', 'delta', 'weight')
    readonly_fields = fields
    list_display = fields
    list_filter = ('format__name',)
    ordering = ('format_id', 'weight')

    def format_name(self, obj):
        return obj.format.name


admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.Filter, FilterAdmin)
