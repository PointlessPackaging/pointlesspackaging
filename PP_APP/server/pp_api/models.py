from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django_resized import ResizedImageField


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
    top_img = ResizedImageField(size=[600, 300], force_format='JPEG', upload_to=top_img_path, null=False,blank=False)
    side_img = ResizedImageField(size=[600, 300], force_format='JPEG', upload_to=side_img_path, null=False,blank=False)
    infer_img = ResizedImageField(size=[600, 300], force_format='JPEG', upload_to=infer_img_path, null=True,blank=True)
    date_posted = models.DateTimeField(default=timezone.now)


class PredictedImagePost(models.Model):
    img_post = models.ForeignKey(ImagePost, on_delete=models.CASCADE)
    packager = models.ForeignKey(Packager, on_delete=models.CASCADE, blank=True, null=True)
    materials = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    outer_size = models.IntegerField(null=True, blank=True)
    inner_size = models.IntegerField(null=True, blank=True)
    item_size = models.IntegerField(null=True, blank=True)
