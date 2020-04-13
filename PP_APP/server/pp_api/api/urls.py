from django.urls import path
from pp_api.api.views import (
    get_hello_rest,
    update_hello_rest,
    delete_hello_rest,
    create_hello_rest,
    upload_imgs,
    delete_post,
    display_feed_view,
)

app_name = 'pp_api'

urlpatterns = [
    path('display_feed', display_feed_view.as_view(), name='display'),
    path('upload', upload_imgs, name='upload'),
    path('delete', delete_post, name='delete'),
    path('get_hello', get_hello_rest, name='detail'),
    path('update_hello', update_hello_rest, name='detail'),
    path('delete_hello', delete_hello_rest, name='detail'),
    path('create_hello', create_hello_rest, name='detail'),
]
