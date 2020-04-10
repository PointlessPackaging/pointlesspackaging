from django.contrib import admin

# Register your models here.
from .models import hello_rest
from .models import image_post

#These register the models with the admin classes.
admin.site.register(hello_rest)
admin.site.register(image_post)