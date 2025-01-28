from django.urls import path
from .views import get_csrf_token
# from .views import get_csrf_token, login_view, signup_view

urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf_token'),
    # path('api/login/', login_view, name='login'),
    # path('api/signup/', signup_view, name='signup'),
]
