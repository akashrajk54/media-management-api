from rest_framework import serializers
from backends_engine.models import VideoUpload, TrimmedVideo, MergedVideo


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


class TrimmedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrimmedVideo
        fields = ["id", "parent_video", "start_time", "end_time", "file", "duration", "created_at"]
        read_only_fields = ["file", "duration", "created_at"]


class MergedVideoSerializer(serializers.ModelSerializer):
    trimmed_videos = serializers.PrimaryKeyRelatedField(queryset=TrimmedVideo.objects.all(), many=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = MergedVideo
        fields = ["id", "trimmed_videos", "file", "duration", "created_at"]
        read_only_fields = ["file", "duration", "created_at"]

    def validate_trimmed_videos(self, value):
        """
        Ensure that at least two trimmed videos are provided.
        """
        if len(value) < 2:
            raise serializers.ValidationError("At least two trimmed videos are required to merge.")
        return value
