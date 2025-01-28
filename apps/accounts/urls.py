from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('check-user-exists/', check_user_exists, name='check_user_exists'),
    path('signin/', signin_view, name='signin'),
    path('signup/', signup_view, name='signup'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]