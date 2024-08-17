from django.contrib import admin
from backends_engine.models import (VideoUpload, TrimmedVideo, MergedVideo)

admin.site.register(VideoUpload)
admin.site.register(TrimmedVideo)
admin.site.register(MergedVideo)
