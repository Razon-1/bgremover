from django.contrib import admin
from .models import ImageJob

@admin.register(ImageJob)
class ImageJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'model_used', 'created_at')
    list_filter = ('status', 'model_used')
