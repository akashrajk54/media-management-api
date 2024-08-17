import factory
from django.contrib.auth import get_user_model
from backends_engine.models import VideoUpload, TrimmedVideo, MergedVideo

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


class TrimmedVideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrimmedVideo

    parent_video = factory.SubFactory(VideoUploadFactory)
    start_time = 0.0
    end_time = 10.0
    file = factory.django.FileField(filename="trimmed_test.mp4")
    duration = 10.0


import factory
from backends_engine.models import MergedVideo

class MergedVideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MergedVideo

    file = factory.django.FileField(filename="merged_test.mp4")
    duration = 20.0

    @factory.post_generation
    def trimmed_videos(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of trimmed_videos was passed in, use them
            for trimmed_video in extracted:
                self.trimmed_videos.add(trimmed_video)
        else:
            # Otherwise, create some trimmed videos
            trimmed_video1 = TrimmedVideoFactory(start_time=0.0, end_time=10.0)
            trimmed_video2 = TrimmedVideoFactory(start_time=10.0, end_time=20.0)
            self.trimmed_videos.add(trimmed_video1, trimmed_video2)
