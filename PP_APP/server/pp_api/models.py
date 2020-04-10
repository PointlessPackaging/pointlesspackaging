from django.db import models
from django.conf import settings

# Create your models here.

class hello_rest(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    msg = models.CharField(max_length=250, null=False, blank=False)

def upload_top_location(instance, filename):
    return 'top/{author_id}/{filename}'.format(author_id=str(instance.user_id.id), filename=filename)

def upload_side_location(instance, filename):
    return 'side/{author_id}/{filename}'.format(author_id=str(instance.user_id.id), filename=filename)

class image_post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    packager = models.CharField(max_length=30, blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1,blank=True, null=True)
    top_img = models.ImageField(upload_to=upload_top_location, null=False,blank=False)
    side_img = models.ImageField(upload_to=upload_side_location, null=False,blank=False)