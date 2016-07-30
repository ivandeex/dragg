from django.contrib import admin
from lib.admin import ReadonlyModelAdmin
from nav import models


class UrlAliasAdmin(ReadonlyModelAdmin, admin.ModelAdmin):
    model = models.UrlAlias
    fields = ('src', 'dst', 'language')
    list_display = fields
    list_filter = ('language',)
    readonly_fields = fields
    search_fields = ('dst',)
    ordering = ('src',)


admin.site.register(models.UrlAlias, UrlAliasAdmin)
