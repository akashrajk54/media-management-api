import uuid
from django.db import models
from django.core.exceptions import ValidationError
import os


def validate_video_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".mp4", ".avi", ".mov", ".mkv"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension: {ext}. Allowed extensions are: {", ".join(valid_extensions)}'
        )


class VideoUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to="videos/", validators=[validate_video_file_extension])
    file_size = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} uploaded at {self.uploaded_at}"


def get_trimmed_video_upload_path(instance, filename):
    # Constructs a path under 'MEDIA_ROOT/trimmed_videos/<filename>'
    return os.path.join("trimmed_videos", filename)


class TrimmedVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name="trimmed_clips")
    start_time = models.FloatField(help_text="Start time in seconds")
    end_time = models.FloatField(help_text="End time in seconds")
    file = models.FileField(
        upload_to=get_trimmed_video_upload_path, validators=[validate_video_file_extension], null=True, blank=True
    )
    duration = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trimmed video {self.id} from {self.start_time} to {self.end_time} seconds"


class MergedVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trimmed_videos = models.ManyToManyField(TrimmedVideo, related_name="merged_videos")
    file = models.FileField(
        upload_to="merged_videos/", validators=[validate_video_file_extension], null=True, blank=True
    )
    duration = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merged video {self.id} created from trimming clips"
