from rest_framework import serializers
from backends_engine.models import VideoUpload


class UploadedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ["id", "file", "file_size", "duration", "uploaded_at"]
        read_only_fields = ["file_size", "duration", "uploaded_at"]

    def validate_file(self, value):
        if not value:
            raise serializers.ValidationError("No video file was provided. Please upload a valid video file.")

        if not hasattr(value, "file"):
            raise serializers.ValidationError(
                "The submitted data was not recognized as a file. Please check and try again."
            )

        return value
