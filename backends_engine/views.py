from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from backends_engine.authentication import StaticTokenAuthentication

from rest_framework import viewsets, status
from rest_framework.response import Response
from backends_engine.models import VideoUpload
from backends_engine.serializers import UploadedVideoSerializer
from backends_engine.utils import success_true_response, success_false_response, validate_single_file_upload
from django.conf import settings
from django.core.exceptions import ValidationError
from backends_engine.media_processor import OpenCVMediaProcessor


@api_view(["GET"])
def Home(request):
    return Response({"success": True})


@csrf_exempt
@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def authentication_check_view(request):
    return Response({"message": "This is a response from the static token authenticated view"})


@authentication_classes([StaticTokenAuthentication])
class UploadedVideoViewSet(viewsets.ModelViewSet):
    queryset = VideoUpload.objects.all()
    serializer_class = UploadedVideoSerializer
    media_processor_class = OpenCVMediaProcessor

    def create(self, request, *args, **kwargs):
        try:
            validate_single_file_upload(request)
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                error_message = next(iter(serializer.errors.values()))[0]
                return Response(success_false_response(message=error_message), status=status.HTTP_400_BAD_REQUEST)

            media_file = serializer.validated_data["file"]
            processor = self.media_processor_class(media_file)

            file_size, duration = processor.validate_media(
                max_size_mb=settings.MAX_VIDEO_SIZE_MB,
                min_duration=settings.MIN_VIDEO_DURATION_SEC,
                max_duration=settings.MAX_VIDEO_DURATION_SEC,
            )

            video_instance = serializer.save(file_size=file_size, duration=duration)
            return Response(
                success_true_response(message="Video uploaded successfully", data={"id": str(video_instance.id)}),
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            message = " ".join(e.messages)
            return Response(success_false_response(message=message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                success_false_response(message="An unexpected error occurred: " + str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
