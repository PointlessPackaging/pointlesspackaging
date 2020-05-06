from django.shortcuts import render, redirect
#from .. import pp_api.models
from pp_api.models import Packager

# Create your views here.
def home_view(request):
    return render(request, 'home.html', {'title': 'Home', 'page_name':'home'})

def rate_view(request):
    return render(request, 'rate.html', {'title' : 'Rate', 'page_name':'rate'})

def feed_view(request):
    return render(request, 'feed.html', {'title' : 'Feed', 'page_name':'feed'})

def ranking_view(request):    
    context = {
        'title': 'Ranking',
        'page_name' : 'ranking',
        'companies' : Packager.objects.all()
    }
    return render(request, 'ranking.html', context)

def about_view(request):
    return render(request, 'about.html', {'title' : 'About', 'page_name':'about'})

def upload_view(request):
    return render(request, 'upload.html', {'title' : 'Upload'})

def success_view(request):
    return render(request, 'success.html', {'title' : 'Success!'})

def charts_view(request, *args, **kwargs):
    return render(request, 'charts.html', {'title' : 'Charts'})

def tables_view(request, *args, **kwargs):
    return render(request, 'tables.html', {'title' : 'Tables'})
