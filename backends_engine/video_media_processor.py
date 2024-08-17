import os
import tempfile
from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime

from media_management import settings
from .base_media_processor import BaseMediaProcessor
from django.core.exceptions import ValidationError


class VideoMediaProcessor(BaseMediaProcessor):
    def calculate_duration(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            for chunk in self.media_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            with VideoFileClip(temp_file_path) as clip:
                duration = clip.duration
        except Exception as e:
            raise ValidationError(f"Cannot calculate duration of the media file: {str(e)}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return duration

    def trim_media(self, start_time, end_time):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            for chunk in self.media_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Ensure the directory exists
        output_directory = os.path.join(settings.MEDIA_ROOT, "trimmed_videos/")
        os.makedirs(output_directory, exist_ok=True)

        # Construct the output file path with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = os.path.splitext(os.path.basename(self.media_file.name))[0]
        output_file = os.path.join(output_directory, f"{file_name}_trimmed_{timestamp}.mp4")

        try:
            with VideoFileClip(temp_file_path) as clip:
                trimmed_clip = clip.subclip(start_time, end_time)
                trimmed_clip.write_videofile(output_file, codec="libx264")
        except Exception as e:
            raise ValidationError(f"Cannot trim media file: {str(e)}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        # Return the path relative to MEDIA_URL
        return os.path.relpath(output_file, settings.MEDIA_ROOT)

    def merge_media(self, media_files):
        clips = []
        try:
            for media_file in media_files:
                clip = VideoFileClip(media_file.path)
                clips.append(clip)

            final_clip = concatenate_videoclips(clips)
            output_file = f"merged_videos/merged_{os.path.basename(media_files[0].name)}"
            final_clip.write_videofile(output_file, codec="libx264")
        except Exception as e:
            raise ValidationError(f"Cannot merge media files: {str(e)}")
        finally:
            for clip in clips:
                clip.close()

        return output_file
