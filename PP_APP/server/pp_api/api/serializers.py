from rest_framework import serializers

from pp_api.models import (
    hello_rest,
    image_post,
)

class hello_rest_serializer(serializers.ModelSerializer):
    class Meta:
        model = hello_rest
        fields = '__all__'
        
class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_post
        fields = ['packager','score','top_img','side_img']

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_post
        fields = ['packager','top_img','side_img']