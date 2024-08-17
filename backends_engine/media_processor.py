import os
import cv2
import tempfile
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError


class MediaProcessor(ABC):
    def __init__(self, media_file):
        self.media_file = media_file

    def calculate_file_size(self):
        file_size_in_mb = self.media_file.size / (1024 * 1024)
        return file_size_in_mb

    @abstractmethod
    def calculate_duration(self):
        """Calculate the duration of the media file."""
        pass

    def validate_media(self, max_size_mb, min_duration, max_duration):
        file_size = self.calculate_file_size()
        duration = self.calculate_duration()

        if file_size > max_size_mb:
            raise ValidationError(f"File size exceeds the maximum limit of {max_size_mb} MB.")

        if not (min_duration <= duration <= max_duration):
            raise ValidationError(f"Media duration must be between {min_duration} and {max_duration} seconds.")

        return file_size, duration


class OpenCVMediaProcessor(MediaProcessor):
    def calculate_duration(self):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            for chunk in self.media_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        cap = cv2.VideoCapture(temp_file_path)
        if not cap.isOpened():
            os.remove(temp_file_path)
            raise ValidationError("Cannot open media file.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        cap.release()
        os.remove(temp_file_path)

        return duration
