from django.urls import path
from django.conf.urls.static import static
from backends_engine.views import (
    Home,
    authentication_check_view,
    UploadedVideoViewSet,
    TrimmedVideoViewSet,
    MergedVideoViewSet,
    LinkSharingViewSet,
    SharedVideoView,
)
from media_management import settings
from rest_framework import routers

router = routers.SimpleRouter()

router.register("videos", UploadedVideoViewSet, basename="videos")
router.register("trimmed-video", TrimmedVideoViewSet, basename="trimmed-video")
router.register("merge-video", MergedVideoViewSet, basename="merge-video")
router.register("link-share", LinkSharingViewSet, basename="link-share")

urlpatterns = [
    path("", Home, name="home"),
    path("auth-check/", authentication_check_view, name="authentication_check_view"),
    path("access-shared-video/", SharedVideoView.as_view(), name="access-shared-video"),
] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
