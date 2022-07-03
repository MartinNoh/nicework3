from django.contrib import admin
from .models import BslHistory


class BslAdmin(admin.ModelAdmin):
    list_display = ('employee', 'contents', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('employee', 'contents')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee', 'contents', 'updated_at'),
        }),
    )
    search_fields = ('employee__realname', 'contents')
    ordering = ('created_at', 'contents')
    filter_horizontal = ()


admin.site.register(BslHistory, BslAdmin)