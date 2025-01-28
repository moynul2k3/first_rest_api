from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
# from .models import User
User = get_user_model()

class EmailAuthBackend(BaseBackend):
    """
    Authenticate using an email address and password.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        # In Django 3.0+, "username" is used as the key for the email.
        try:
            user = User.objects.get(email=email)
            print('user found')
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            print('user not found')
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model


# class EmailAuthBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None):
#         try:
#             user = get_user_model().objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except get_user_model().DoesNotExist:
#             return None
