from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='media/')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Image resize before upload
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

<<<<<<< HEAD:PP_APP/server/frontend/models.py
# Create your models here.
=======
>>>>>>> 875bb30... update:epp/web/epp/users/models.py
