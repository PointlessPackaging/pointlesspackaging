from django.urls import path
from pp_api.api.views import (
    upload_imgs,
    delete_post,
    display_feed_view,
    ChartData,
)

app_name = 'pp_api'

urlpatterns = [
    path('display_feed', display_feed_view.as_view(), name='display'),
    path('upload', upload_imgs, name='upload'),
    path('delete', delete_post, name='delete'),
    path('chart_data/', ChartData.as_view()),
]
