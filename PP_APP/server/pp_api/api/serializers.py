from rest_framework import serializers

from pp_api.models import (
<<<<<<< HEAD
    image_post,
    image_post_predicted,
=======
    # hello_rest,
    PPUsers,
    Packager,
    ImagePost,
    PredictedImagePost,
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.
)

# class hello_rest_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = hello_rest
#         fields = '__all__'
<<<<<<< HEAD
        
=======

class PPUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPUsers
        fields = '__all__'

class PackagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packager
        fields = ['name','display_name', 'count','score']

>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.
class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictedImagePost
        fields = ['img_post_id','packager', 'outer_size','inner_size','item_size']

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['top_img','side_img','infer_img']

class PredictedSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictedImagePost
        fields = ['img_post_id', 'packager', 'score', 'outer_size','inner_size','item_size']