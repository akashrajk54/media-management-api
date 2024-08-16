from django.urls import path
from backends_engine.views import Home, authentication_check_view

urlpatterns = [
    path("", Home, name="home"),
    path("auth-check/", authentication_check_view, name="authentication_check_view"),
]
