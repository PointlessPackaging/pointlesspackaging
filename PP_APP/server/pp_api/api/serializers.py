from rest_framework import serializers

from pp_api.models import (
    hello_rest,
    image_post,
    image_post_predicted,
)

class hello_rest_serializer(serializers.ModelSerializer):
    class Meta:
        model = hello_rest
        fields = '__all__'
        
class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_post_predicted
        fields = ['img_post_id','packager','infer_img', 'outerbox','innerbox','item']

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_post
        fields = ['top_img','side_img']

class PredictedSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_post_predicted
        fields = ['img_post_id', 'packager', 'score', 'infer_img', 'outerbox','innerbox','item']