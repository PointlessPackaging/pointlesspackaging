from django.contrib import admin

# Register your models here.
from pp_api.models import (
    #hello_rest,
    image_post,
    image_post_predicted,
)

#These register the models with the admin classes.
#admin.site.register(hello_rest)
admin.site.register(image_post)
admin.site.register(image_post_predicted)
