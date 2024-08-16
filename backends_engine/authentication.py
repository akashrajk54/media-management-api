from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
logger_error = logging.getLogger("error")


class StaticTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            message = "No API token provided."
            logger_error.error(message)
            raise AuthenticationFailed(message)

        expected_token = settings.API_STATIC_TOKEN

        if token != expected_token:
            message = "Invalid API token."
            logger_error.error(message)
            raise AuthenticationFailed(message)

        return None, token
