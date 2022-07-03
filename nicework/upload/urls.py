from django.urls import path
from .views import registration

app_name = 'upload'

urlpatterns = [
    path('regt', registration, name='regt'),
]