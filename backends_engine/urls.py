from django.urls import path
from django.conf.urls.static import static
from backends_engine.views import Home, authentication_check_view, UploadedVideoViewSet
from media_management import settings
from rest_framework import routers

router = routers.SimpleRouter()

router.register("videos", UploadedVideoViewSet, basename="videos")

urlpatterns = [
    path("", Home, name="home"),
    path("auth-check/", authentication_check_view, name="authentication_check_view"),
] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
