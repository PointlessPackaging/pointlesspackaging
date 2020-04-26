from django.db import models
from django.conf import settings

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage

# Create your models here.

""" Django basic reference model """
# class hello_rest(models.Model):
#     name = models.CharField(max_length=20, null=False, blank=False)
#     msg = models.CharField(max_length=250, null=False, blank=False)

def upload_top_location(instance, filename):
    return 'top/{author_id}/{filename}'.format(author_id=str(instance.user_id.id), filename=filename)

def upload_side_location(instance, filename):
    return 'side/{author_id}/{filename}'.format(author_id=str(instance.user_id.id), filename=filename)

def upload_infer_location(instance, filename):
    return 'infer/{author_id}/{filename}'.format(author_id=str(instance.user_id.id), filename=filename)

class image_post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    top_img = models.ImageField(upload_to=upload_top_location, null=False,blank=False)
    side_img = models.ImageField(upload_to=upload_side_location, null=False,blank=False)

    def create(self, validated_data):
        return image_post(**validated_data)

    ## https://stackoverflow.com/questions/30434323/django-resize-image-before-upload
    def save(self, *args, **kwargs):
        pil_image_obj = Image.open(self.top_img)
        if pil_image_obj.size[1] > 300:
            new_image = resizeimage.resize_height(pil_image_obj, 300)
            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')

            temp_name = self.top_img.name
            self.top_img.delete(save=False)  

            self.top_img.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

        pil_image_obj = Image.open(self.side_img)
        if pil_image_obj.size[1] > 300:
            new_image = resizeimage.resize_height(pil_image_obj, 300)
            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')

            temp_name = self.side_img.name
            self.side_img.delete(save=False)  

            self.side_img.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

        super(image_post, self).save(*args, **kwargs)

class image_post_predicted(models.Model):
    img_post_id = models.ForeignKey(image_post, on_delete=models.CASCADE)
    packager = models.CharField(max_length=30, null=True, blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1,blank=True, null=True)
    infer_img = models.ImageField(null=True,blank=True)
    outerbox = models.IntegerField(null=True,blank=True)
    innerbox = models.IntegerField(null=True,blank=True)
    item = models.IntegerField(null=True,blank=True)
