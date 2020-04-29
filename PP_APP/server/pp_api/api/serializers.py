from rest_framework import serializers

from pp_api.models import (
    PPUsers,
    Packager,
    ImagePost,
    PredictedImagePost,
)

class PPUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPUsers
        fields = '__all__'

class PackagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packager
        fields = ['name','display_name', 'count','score']

class PredictedImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictedImagePost
        fields = ['img_post_id','packager', 'outer_size','inner_size','item_size']

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['top_img','side_img','infer_img']

class DisplayImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'top_img','side_img','infer_img','date_posted']

class DisplayFeedSerializer(serializers.ModelSerializer):
    img_post_id = DisplayImagePostSerializer(many=False, read_only=True)
    packager = PackagerSerializer(many=False, read_only=True)
    class Meta:
        model = PredictedImagePost
        fields = ['img_post_id', 'packager', 'score', 'materials', 'outer_size','inner_size','item_size',]