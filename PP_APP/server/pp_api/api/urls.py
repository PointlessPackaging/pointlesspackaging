from django.urls import path
from pp_api.api.views import (
    upload_imgs,
    update_img_post,
    delete_post,
    display_feed_view,
    search_packager_posts_view,
    search_user_posts_view,
    display_all_packagers_view,
    top_five_best_view,
    top_five_worst_view,
    ChartData,
    TableData,
)

app_name = 'pp_api'

urlpatterns = [
    path('display_feed', display_feed_view.as_view(), name='Display All Posts'),
    path('search_packager_posts', search_packager_posts_view.as_view(), name='Search Packager Posts'),
    path('search_user_posts', search_user_posts_view.as_view(), name='Search User Posts'),
    path('display_all_packagers', display_all_packagers_view.as_view(), name='Display All Packagers'),
    path('best_five', top_five_best_view, name='Top 5 Best'),
    path('worst_five', top_five_worst_view, name='Top 5 Worst'),
    path('upload', upload_imgs, name='upload'),
    path('update', update_img_post, name='update'),
    # path('delete', delete_post, name='delete'),
    path('chart_data/', ChartData.as_view()),
    path('table_data/', TableData.as_view()),
]
