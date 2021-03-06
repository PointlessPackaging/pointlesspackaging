from django.urls import path
from .views import (
    home_view,
    rate_view,
    FeedView,
    ranking_view,
    about_view,
    upload_view,
    success_view,
    charts_view,
    tables_view,
    post_view,
    not_found_404,
    feedback_view,
)

app_name = 'frontend'

urlpatterns = [
    path('', home_view, name='home'),
    path('rate/', rate_view, name='rate'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('ranking/', ranking_view, name='ranking'),
    path('about/', about_view, name='about'),
    path('upload/', upload_view, name='upload'),
    path('success/', success_view, name='success'),
    path('charts/', charts_view, name='charts'),
    path('tables/', tables_view, name='tables'),
    path('feed/<int:post_id>/', post_view, name="pp_post"), # Ex. /feed/455/
    path('feedback/', feedback_view, name='feedback'),
]
