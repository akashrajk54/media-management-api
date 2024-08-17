import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from backends_engine.models import VideoUpload
from backends_engine.factories import UserFactory
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


@pytest.mark.django_db
class TestUploadedVideoViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("videos-list")

    @patch("backends_engine.media_processor.OpenCVMediaProcessor.validate_media", return_value=(5.0, 10.0))
    def test_upload_video_success(self, mock_validate_media):
        video_data = SimpleUploadedFile("test_video.mp4", b"fake_video_content", content_type="video/mp4")

        data = {"file": video_data}

        response = self.client.post(self.url, data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert VideoUpload.objects.count() == 1
        assert "id" in response.data["data"]

    @patch("backends_engine.media_processor.OpenCVMediaProcessor.validate_media", return_value=(5.0, 10.0))
    def test_upload_no_file_provided(self, mock_validate_media):
        data = {}

        response = self.client.post(self.url, data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "No video file was provided. Please upload a valid video file."
        assert VideoUpload.objects.count() == 0

    @patch("backends_engine.media_processor.OpenCVMediaProcessor.validate_media", return_value=(5.0, 10.0))
    def test_upload_invalid_file_format(self, mock_validate_media):
        invalid_file = tempfile.NamedTemporaryFile(suffix=".txt").name
        file_data = SimpleUploadedFile(invalid_file, b"invalid_content", content_type="text/plain")

        data = {"file": file_data}

        response = self.client.post(self.url, data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Unsupported file extension" in response.data["message"]
        assert VideoUpload.objects.count() == 0
