from django.urls import path
from .views import (
    home_view,
    about_view,
    upload_view

)

#app_name = 'frontend'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('upload/', upload_view, name='upload')
]
