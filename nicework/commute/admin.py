from django.contrib import admin
from .models import CmtHistory


class CmtAdmin(admin.ModelAdmin):
    list_display = ('employee', 'weeknum', 'todaycat', 'startdatetime', 'enddatetime', 'workinghours', 'breaktime', 'overtime', 'is_abnormal')
    fieldsets = (
        (None, {'fields': ('employee',)}),
        ('Today', {'fields': ('weeknum', 'todaycat',)}),
        ('Work info', {'fields': ('startdatetime', 'enddatetime', 'workinghours', 'breaktime', 'overtime')}),
        ('is_abnormal', {'fields': ('is_abnormal', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee', 'weeknum', 'todaycat', 'startdatetime', 'enddatetime', 'workinghours', 'breaktime', 'overtime', 'is_abnormal'),
        }),
    )
    search_fields = ('employee__realname', 'weeknum', 'todaycat')
    ordering = ('startdatetime', 'todaycat')
    filter_horizontal = ()


admin.site.register(CmtHistory, CmtAdmin)