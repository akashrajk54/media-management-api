from django.contrib import admin
from backends_engine.models import (VideoUpload, TrimmedVideo)

admin.site.register(VideoUpload)
admin.site.register(TrimmedVideo)
