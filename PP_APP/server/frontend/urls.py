from django.urls import path
from .views import (
    home_view,
    about_view,
    upload_view,
    success_view,
    charts_view,
    tables_view,
)

#app_name = 'frontend'

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('upload/', upload_view, name='upload'),
    path('success/', success_view, name='success'),
    path('charts/', charts_view, name='charts'),
    path('tables/', tables_view, name='tables'),
]
