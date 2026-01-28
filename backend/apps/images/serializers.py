from rest_framework import serializers
from .models import ImageJob

class ImageJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageJob
        fields = '__all__'
