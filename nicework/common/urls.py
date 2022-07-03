from django.urls import path
from django.contrib.auth import views as auth_views
from .views import accounts_views, base_views

app_name = 'common'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
    path('policy/', base_views.privacy_policy, name='policy'),
    path('terms/', base_views.terms_of_service, name='terms'),

    # accounts_views.py
    path('signup/', accounts_views.signup, name='signup'),
    path('mypage/', accounts_views.mypage, name='mypage'),
    path('mypage/password/', accounts_views.password, name='password'),

    # auth_views.py
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # send test email
    path('send_email/', accounts_views.send_email, name='send_email'),

    # activate email
    path('activate/<str:uidb64>/<str:token>/', accounts_views.activate, name="activate"),
]