from django.db import models


class Uploader(models.Model):
    title = models.CharField(blank=False, max_length=120)
    epp_image = models.ImageField(upload_to='images/', blank=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f'{self.epp_image}'
