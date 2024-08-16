from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from backends_engine.utils import success_false_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response_data = success_false_response(message=str(exc))
        return JsonResponse(response_data, status=response.status_code)

    return response
