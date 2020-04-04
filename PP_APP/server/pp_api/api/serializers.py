from rest_framework import serializers

from pp_api.models import (
    PPUsers,
    Packager,
    ImagePost,
    PredictedImagePost,
)

class PPUsersSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = PPUsers
        fields = '__all__'

class PackagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packager
        fields = ['name','brand_name', 'count','score']

class PredictedImagePostSerializer(serializers.ModelSerializer):
=======
        #model = hello_rest
        fields = '__all__'

class ImagePostSerializer(serializers.ModelSerializer):
>>>>>>> 6f72ecb... This is the beginning of the design of the website, with styling and a designed layout.
    class Meta:
        model = PredictedImagePost
        fields = ['img_post', 'outer_size','inner_size','item_size']

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['top_img','side_img','infer_img']

class DisplayPackagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packager
        fields = ['brand_name', 'score']

class DisplayImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'top_img','side_img','infer_img','date_posted']

class DisplayFeedSerializer(serializers.ModelSerializer):
    img_post = DisplayImagePostSerializer(many=False, read_only=True)
    packager = DisplayPackagerSerializer(many=False, read_only=True)
    class Meta:
<<<<<<< HEAD
        model = PredictedImagePost
        fields = ['img_post', 'packager', 'score', 'materials', 'outer_size','inner_size','item_size',]
=======
        model = image_post_predicted
        fields = ['img_post_id', 'packager', 'score', 'infer_img', 'outerbox','innerbox','item']
>>>>>>> 6f72ecb... This is the beginning of the design of the website, with styling and a designed layout.
