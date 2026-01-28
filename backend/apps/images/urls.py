from django.urls import path
from .views import process_image_view

urlpatterns = [
    path('process/', process_image_view, name='process_image'),
]