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
