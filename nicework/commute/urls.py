from django.urls import path

from .views import regt_views, hist_views

app_name = 'commute'

urlpatterns = [    
    path('regt/<str:check_result>/', regt_views.registration, name='regt'),    

    path('hist/', hist_views.history, name='hist'),
    path('situ/', hist_views.situation, name='situ'),
    path('toth/', hist_views.totalhistory, name='toth'),

    path('ovtr/', regt_views.overtimeregt, name='ovtr'),
    
    path('ovth/', hist_views.overtimehist, name='ovth'),
    path('delt/<int:myreg_id>/', hist_views.delete, name='delt'),

    path('ovtw/', hist_views.overtimewait, name='ovtw'),
    path('aprv/', hist_views.overtimeaprv, name='aprv'),
    path('ovts/', hist_views.overtimesitu, name='ovts'),
    path('ovtt/', hist_views.overtimetoth, name='ovtt'),
]