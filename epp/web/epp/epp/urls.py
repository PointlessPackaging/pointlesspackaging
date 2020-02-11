"""epp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
=======
from django.contrib.auth import views as auth_views
from django.urls import path, include
>>>>>>> 875bb30... update
from django.conf import settings
from django.conf.urls.static import static
from uploader.views import home_view, get_data, success_view

from uploader.views import ChartData



urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('success/', success_view, name='success'),

    path('api/data/', get_data, name='api-data'),
    path('api/chart/data/', ChartData.as_view()),
    # url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^api/data/$', get_data, name='api-data'),
    # url(r'^api/chart/data/$', ChartData.as_view()),
    # path('line_chart/', line_chart, name='home'),
    # path('line_chart/json/', line_chart_json, name='line_chart_json'),
    # path('epp_images/', display_epp_images, name='epp_images'),
<<<<<<< HEAD
=======

    # TODO:
    path('admin/', admin.site.urls),
    path('pp_api/', include('pp_api.urls')),
    path('profile/', user_views.profile_view, name='profile'),
    path('register/', user_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
>>>>>>> 875bb30... update
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
