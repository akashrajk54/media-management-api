import factory
from django.contrib.auth import get_user_model
from backends_engine.models import VideoUpload

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class VideoUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoUpload

    file = factory.django.FileField(filename="test.mp4")
    file_size = 10.5
    duration = 120.0
