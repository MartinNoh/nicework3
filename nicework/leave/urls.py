from django.urls import path

from .views import regt_views, hist_views

app_name = 'leave'

urlpatterns = [
    path('regt/', regt_views.registration, name='regt'),

    path('hist/', hist_views.history, name='hist'),
    path('delt/<int:myreg_id>/', hist_views.delete, name='delt'),

    path('situ/', hist_views.situation, name='situ'),
    path('wait/', hist_views.waiting, name='wait'),
    path('aprv/', hist_views.approval, name='aprv'),
    path('toth/', hist_views.totalhistory, name='toth'),

    path('cldr/', hist_views.calendar, name='cldr'),    
]