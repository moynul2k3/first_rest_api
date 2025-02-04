from django.urls import path
from .views import *
# from .views import get_csrf_token, login_view, signup_view

urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf_token'),
    path('banners/', BannerView.as_view(), name='banners'),
]
