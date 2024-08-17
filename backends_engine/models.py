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
