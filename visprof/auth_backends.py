from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class OAuthBackend(ModelBackend):

    def authenticate(self, request, email=None, access_token=None):
        # pylint: disable=arguments-differ
        if email is None or access_token is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email)
        return user
