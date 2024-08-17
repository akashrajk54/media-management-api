import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from backends_engine.models import VideoUpload, TrimmedVideo, MergedVideo
from backends_engine.factories import UserFactory, VideoUploadFactory, TrimmedVideoFactory
from backends_engine.video_media_processor import VideoMediaProcessor
import tempfile
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


@pytest.mark.django_db
class TestUploadedVideoViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("videos-list")

    @patch("backends_engine.video_media_processor.VideoMediaProcessor.validate_media", return_value=(5.0, 10.0))
    def test_upload_video_success(self, mock_validate_media):
        video_data = SimpleUploadedFile("test_video.mp4", b"fake_video_content", content_type="video/mp4")

        data = {"file": video_data}

        response = self.client.post(self.url, data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert VideoUpload.objects.count() == 1
        assert "id" in response.data["data"]

    @patch("backends_engine.video_media_processor.VideoMediaProcessor.validate_media", return_value=(5.0, 10.0))
    def test_upload_no_file_provided(self, mock_validate_media):
        data = {}

        response = self.client.post(self.url, data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "No video file was provided. Please upload a valid video file."
        assert VideoUpload.objects.count() == 0

    @patch("backends_engine.video_media_processor.VideoMediaProcessor.validate_media", return_value=(5.0, 10.0))
    def test_upload_invalid_file_format(self, mock_validate_media):
        invalid_file = tempfile.NamedTemporaryFile(suffix=".txt").name
        file_data = SimpleUploadedFile(invalid_file, b"invalid_content", content_type="text/plain")

        data = {"file": file_data}

        response = self.client.post(self.url, data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Unsupported file extension" in response.data["message"]
        assert VideoUpload.objects.count() == 0


@pytest.mark.django_db
class TestTrimmedVideoViewSet:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("trimmed-video-list")

    def test_create_trimmed_video_missing_parent_video_or_trims(self):
        response = self.client.post(self.url, {"parent_video": None, "trims": []}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Please provide 'parent_video' and 'trims'."

    @patch("backends_engine.video_media_processor.VideoMediaProcessor.trim_media", return_value="path/to/trimmed_video.mp4")
    def test_create_trimmed_video_success(self, mock_trim_media):
        parent_video = VideoUploadFactory()
        trims = [{"start_time": 2, "end_time": 5}]
        data = {
            "parent_video": str(parent_video.id),
            "trims": trims,
        }

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data["data"]) == 1
        assert TrimmedVideo.objects.count() == 1

    @patch("backends_engine.video_media_processor.VideoMediaProcessor.trim_media", side_effect=ValidationError("Cannot trim media file"))
    def test_create_trimmed_video_validation_error(self, mock_trim_media):
        parent_video = VideoUploadFactory()
        trims = [{"start_time": 2, "end_time": 5}]
        data = {
            "parent_video": str(parent_video.id),
            "trims": trims,
        }

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot trim media file" in response.data["message"]

    @patch("backends_engine.video_media_processor.VideoMediaProcessor.trim_media", return_value="path/to/trimmed_video.mp4")
    def test_create_trimmed_video_unexpected_error(self, mock_trim_media):
        parent_video = VideoUploadFactory()
        trims = [{"start_time": 2, "end_time": 5}]
        data = {
            "parent_video": str(parent_video.id),
            "trims": trims,
        }

        with patch("backends_engine.models.TrimmedVideo.objects.create", side_effect=Exception("Unexpected error")):
            response = self.client.post(self.url, data, format="json")
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "An unexpected error occurred" in response.data["message"]


@pytest.mark.django_db
class TestMergedVideoViewSet:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("merge-video-list")

    def test_create_merged_video_missing_trimmed_videos(self):
        response = self.client.post(self.url, {"trimmed_videos": None}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Please provide 'trimmed_videos'."

    def test_create_merged_video_insufficient_trimmed_videos(self):
        trimmed_video = TrimmedVideoFactory()
        data = {"trimmed_videos": [str(trimmed_video.id)]}

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "At least two trimmed videos are required to merge."

    @patch.object(VideoMediaProcessor, 'merge_media', return_value="path/to/merged_video.mp4")
    def test_create_merged_video_success(self, mock_merge_media):
        trimmed_videos = [TrimmedVideoFactory(), TrimmedVideoFactory()]
        data = {"trimmed_videos": [str(tv.id) for tv in trimmed_videos]}

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data["data"]["trimmed_videos"]) == 2
        assert MergedVideo.objects.count() == 1

    @patch.object(VideoMediaProcessor, 'merge_media', side_effect=ValidationError("Cannot merge media files"))
    def test_create_merged_video_validation_error(self, mock_merge_media):
        trimmed_videos = [TrimmedVideoFactory(), TrimmedVideoFactory()]
        data = {"trimmed_videos": [str(tv.id) for tv in trimmed_videos]}

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot merge media files" in response.data["message"]

    @patch.object(VideoMediaProcessor, 'merge_media', return_value="path/to/merged_video.mp4")
    def test_create_merged_video_unexpected_error(self, mock_merge_media):
        trimmed_videos = [TrimmedVideoFactory(), TrimmedVideoFactory()]
        data = {"trimmed_videos": [str(tv.id) for tv in trimmed_videos]}

        with patch("backends_engine.models.MergedVideo.objects.create", side_effect=Exception("Unexpected error")):
            response = self.client.post(self.url, data, format="json")
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "An unexpected error occurred" in response.data["message"]
