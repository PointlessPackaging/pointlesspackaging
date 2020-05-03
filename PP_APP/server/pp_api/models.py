from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage


""" Django basic reference model """


def top_img_path(instance, filename):
    return 'top/{0}/{1}'.format(instance.user_id.id, filename)


def side_img_path(instance, filename):
    return 'side/{0}/{1}'.format(instance.user_id.id, filename)


def infer_img_path(instance, filename):
    return 'infer/{0}/{1}'.format(instance.user_id.id, filename)


class PPUsers(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    def __str__(self):
        return f'by {self.email}'


class Packager(models.Model):
    name = models.CharField(max_length=50, unique=True)
    brand_name = models.CharField(max_length=50, default="-1")
    count = models.IntegerField()
    score = models.FloatField()


class ImagePost(models.Model):
    user_id = models.ForeignKey(PPUsers, on_delete=models.CASCADE)
    top_img = models.ImageField(upload_to=top_img_path, null=False, blank=False)
    side_img = models.ImageField(upload_to=side_img_path, null=False, blank=False)
    infer_img = models.ImageField(upload_to=infer_img_path, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'from ImagePost {self.id}'

    def create(self, validated_data):
        return ImagePost(**validated_data)

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

        super(ImagePost, self).save(*args, **kwargs)


class PredictedImagePost(models.Model):
    img_post = models.ForeignKey(ImagePost, on_delete=models.CASCADE)
    packager = models.ForeignKey(Packager, on_delete=models.CASCADE, blank=True, null=True)
    materials = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    outer_size = models.IntegerField(null=True, blank=True)
    inner_size = models.IntegerField(null=True, blank=True)
    item_size = models.IntegerField(null=True, blank=True)
