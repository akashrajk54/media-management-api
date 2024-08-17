from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from backends_engine.authentication import StaticTokenAuthentication

from rest_framework import viewsets, status
from rest_framework.response import Response
from backends_engine.models import VideoUpload, TrimmedVideo
from backends_engine.serializers import (UploadedVideoSerializer, TrimmedVideoSerializer)
from backends_engine.utils import (success_true_response, success_false_response, validate_single_file_upload)
from django.conf import settings
from django.core.exceptions import ValidationError
from backends_engine.video_media_processor import VideoMediaProcessor
from django.shortcuts import get_object_or_404
import logging


# Set up loggers
logger = logging.getLogger(__name__)
logger_debug = logging.getLogger("debug")
logger_info = logging.getLogger("info")
logger_error = logging.getLogger("error")


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
    media_processor_class = VideoMediaProcessor

    def create(self, request, *args, **kwargs):
        logger_info.info("Received request to upload a video.")
        try:
            # Validate single file upload
            validate_single_file_upload(request)
            logger_debug.debug("File upload validated.")

            # Validate serializer
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                error_message = next(iter(serializer.errors.values()))[0]
                logger_error.error(f"Serializer validation failed: {error_message}")
                return Response(success_false_response(message=error_message), status=status.HTTP_400_BAD_REQUEST)

            media_file = serializer.validated_data["file"]
            processor = self.media_processor_class(media_file)

            # Validate media file
            file_size, duration = processor.validate_media(
                max_size_mb=settings.MAX_VIDEO_SIZE_MB,
                min_duration=settings.MIN_VIDEO_DURATION_SEC,
                max_duration=settings.MAX_VIDEO_DURATION_SEC,
            )
            logger_debug.debug(f"Media validated: file_size={file_size}, duration={duration}")

            # Save the video instance
            video_instance = serializer.save(file_size=file_size, duration=duration)
            logger_info.info(f"Video uploaded successfully with ID: {video_instance.id}")

            return Response(
                success_true_response(message="Video uploaded successfully", data={"id": str(video_instance.id)}),
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            message = " ".join(e.messages)
            logger_error.error(f"Validation error occurred: {message}")
            return Response(success_false_response(message=message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = f"An unexpected error occurred: {str(e)}"
            logger_error.error(message)
            return Response(
                success_false_response(message=message),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TrimmedVideoViewSet(viewsets.ModelViewSet):
    queryset = TrimmedVideo.objects.all()
    serializer_class = TrimmedVideoSerializer

    def create(self, request, *args, **kwargs):
        logger_info.info("Received request to trim video.")

        parent_video_id = request.data.get('parent_video')
        trims = request.data.get('trims')

        if not parent_video_id or not trims:
            message = "Please provide 'parent_video' and 'trims'."
            logger_error.error(message)
            return Response(success_false_response(message=message), status=status.HTTP_400_BAD_REQUEST)

        parent_video = get_object_or_404(VideoUpload, id=parent_video_id)
        logger_debug.debug(f"Parent video retrieved: {parent_video_id}")

        processor = VideoMediaProcessor(parent_video.file)
        trimmed_videos = []

        try:
            for trim in trims:
                start_time = trim.get('start_time')
                end_time = trim.get('end_time')

                if not start_time or not end_time:
                    continue

                trimmed_file_path = processor.trim_media(float(start_time), float(end_time))
                trimmed_video = TrimmedVideo.objects.create(
                    parent_video=parent_video,
                    start_time=float(start_time),
                    end_time=float(end_time),
                    file=trimmed_file_path,
                    duration=float(end_time) - float(start_time)
                )
                trimmed_videos.append(trimmed_video)

            serializer = self.get_serializer(trimmed_videos, many=True)
            logger_info.info(f"Videos trimmed successfully: {[video.id for video in trimmed_videos]}")
            return Response({
                "success": True,
                "message": "Videos trimmed successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            message = " ".join(e.messages)
            logger_error.error(f"Validation error occurred: {message}")
            return Response(success_false_response(message=message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = f"An unexpected error occurred: {str(e)}"
            logger_error.error(message)
            return Response(success_false_response(message=message), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

