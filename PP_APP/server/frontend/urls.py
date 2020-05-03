from django.urls import path
from .views import (
    home_view,
    charts_view,
    tables_view,
)

app_name = 'frontend'

urlpatterns = [
    path('', home_view, name='home'),
    path('charts/', charts_view, name='charts'),
    path('tables/', tables_view, name='tables'),
]
