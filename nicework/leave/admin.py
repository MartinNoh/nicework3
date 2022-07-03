from django.contrib import admin
from .models import Reward, LevHistory
# Register your models here.


class LevAdmin(admin.ModelAdmin):
    list_display = ('employee', 'startdate', 'enddate', 'leaveterm', 'leavecat', 'approval')
    list_filter = ('approval',)
    fieldsets = (
        (None, {'fields': ('employee', 'leaveterm', 'leavecat')}),
        ('Date, Time', {'fields': ('startdate', 'starttime', 'enddate', 'endtime')}),
        ('Approval', {'fields': ('approval',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee', 'leaveterm', 'leavecat', 'startdate', 'starttime', 'enddate', 'endtime', 'approval'),
        }),
    )
    search_fields = ('employee__realname', 'leavecat')
    ordering = ('startdate', 'starttime', 'enddate', 'endtime', 'leavecat')
    filter_horizontal = ()


class RewardAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reason', 'days', 'granter', 'created_at', 'created_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee', 'granter', 'days', 'reason'),
        }),
    )
    search_fields = ('employee__realname', 'reason')
    ordering = ('created_at', 'reason')
    filter_horizontal = ()


admin.site.register(Reward, RewardAdmin)
admin.site.register(LevHistory, LevAdmin)