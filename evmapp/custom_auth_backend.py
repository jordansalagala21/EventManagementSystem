# custom_auth_backend.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class AdminAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_admin:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
