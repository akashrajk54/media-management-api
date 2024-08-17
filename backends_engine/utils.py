from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from urllib.parse import urlencode
from django.core.exceptions import ValidationError


def success_true_response(message=None, data=None, count=None):
    result = dict(success=True)
    result["message"] = message or ""
    result["data"] = data or {}
    if count is not None:
        result["count"] = count
    return result


def success_false_response(message=None, data=None):
    result = dict(success=False)
    result["message"] = message or ""
    result["data"] = data or {}

    return result


def validate_single_file_upload(request, file_key="file"):
    if file_key not in request.FILES or len(request.FILES) != 1:
        if len(request.FILES) > 1:
            raise ValidationError("Only one video file can be uploaded at a time.")
        raise ValidationError("No video file was provided. Please upload a valid video file.")
    return None


def validate_merged_video_request(data):
    merged_video_id = data.get("merged_video_id")

    if not merged_video_id:
        raise ValidationError("Please provide 'merged_video_id' and 'email_addresses'.")

    return merged_video_id


class LinkGenerator:
    signer = TimestampSigner()

    @staticmethod
    def generate_link(merged_video_id, expiry_minutes=30):
        token = LinkGenerator.signer.sign(merged_video_id)
        query_params = urlencode({"token": token})
        return f"{settings.SITE_URL}/access-shared-video/?{query_params}"

    @staticmethod
    def validate_link(token, max_age_minutes=30):
        try:
            merged_video_id = LinkGenerator.signer.unsign(token, max_age=max_age_minutes * 60)
            return merged_video_id
        except SignatureExpired:
            raise ValidationError("The link has expired.")
        except BadSignature:
            raise ValidationError("Invalid link.")
