from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from backends_engine.authentication import StaticTokenAuthentication


@api_view(['GET'])
def Home(request):
    return Response({'success': True})


@csrf_exempt
@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def authentication_check_view(request):
    return Response({"message": "This is a response from the static token authenticated view"})


