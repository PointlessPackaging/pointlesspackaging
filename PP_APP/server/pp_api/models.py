from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
<<<<<<< HEAD
=======
from django.utils import timezone
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage


<<<<<<< HEAD
# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
def top_img_path(instance, filename):
    return 'top/user_{0}/{1}'.format(instance.user.id, filename)


def side_img_path(instance, filename):
    return 'side/user_{0}/{1}'.format(instance.user.id, filename)


class Packager(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    score = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f'{self.name} Packager'


class Post(models.Model):
    top_image = models.ImageField(upload_to=top_img_path)
    side_image = models.ImageField(upload_to=side_img_path)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} Post'

    # TODO: test for resize
    def save(self, *args, **kwargs):
        top_img = Image.open(self.top_image)
        side_img = Image.open(self.side_image)
        output_size = (300, 600)
        if top_img and side_img:
            top_img.thumbnail(output_size)
            side_img.thumbnail(output_size)
        super(Post, self).save(*args, **kwargs)


class PredictedPost(models.Model):
    packager = models.ForeignKey(Packager, on_delete=models.CASCADE, blank=True, null=True)
    materials = models.CharField(max_length=100, blank=True, null=True)
    outer_size = models.IntegerField(blank=True, null=True)
    inner_size = models.IntegerField(blank=True, null=True)
    item_size = models.IntegerField(blank=True, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} PredictedPost'

=======
""" Django basic reference model """
def top_img_path(instance, filename):
    return 'top/{0}/{1}'.format(instance.user_id.id, filename)

def side_img_path(instance, filename):
    return 'side/{0}/{1}'.format(instance.user_id.id, filename)

def infer_img_path(instance, filename):
    return 'infer/{0}/{1}'.format(instance.user_id.id, filename)

class PPUsers(models.Model):
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.

class Packager(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, default="-1")
    count = models.IntegerField()
    score = models.DecimalField(max_digits=2, decimal_places=1)

<<<<<<< HEAD

class image_post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    top_img = models.ImageField(upload_to=top_img_path, null=False, blank=False)
    side_img = models.ImageField(upload_to=side_img_path, null=False, blank=False)
=======
class ImagePost(models.Model):
    user_id = models.ForeignKey(PPUsers, on_delete=models.CASCADE)
    top_img = models.ImageField(upload_to=top_img_path, null=False,blank=False)
    side_img = models.ImageField(upload_to=side_img_path, null=False,blank=False)
    infer_img = models.ImageField(upload_to=infer_img_path, null=True,blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.

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

<<<<<<< HEAD

class image_post_predicted(models.Model):
    img_post_id = models.ForeignKey(image_post, on_delete=models.CASCADE)
    packager = models.CharField(max_length=30, null=True, blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    infer_img = models.ImageField(null=True, blank=True)
    outerbox = models.IntegerField(null=True, blank=True)
    innerbox = models.IntegerField(null=True, blank=True)
    item = models.IntegerField(null=True, blank=True)
=======
class PredictedImagePost(models.Model):
    img_post_id = models.ForeignKey(ImagePost, on_delete=models.CASCADE)
    packager = models.ForeignKey(Packager, on_delete=models.CASCADE, blank=True, null=True)
    materials = models.CharField(max_length=100, blank=True, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1,blank=True, null=True)
    outer_size = models.IntegerField(null=True,blank=True)
    inner_size = models.IntegerField(null=True,blank=True)
    item_size = models.IntegerField(null=True,blank=True)
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.
