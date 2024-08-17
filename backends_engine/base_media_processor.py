from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError


class BaseMediaProcessor(ABC):
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

    @abstractmethod
    def trim_media(self, start_time, end_time):
        """Trim the media from start_time to end_time and return the trimmed media file path."""
        pass

    @abstractmethod
    def merge_media(self, media_files):
        """Merge the given list of media files and return the merged media file path."""
        pass
