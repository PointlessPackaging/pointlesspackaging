from django.shortcuts import render, redirect, get_list_or_404
from pp_api.models import ImagePost, PredictedImagePost, Packager, PPUsers

# Create your views here.
def home_view(request):
    return render(request, 'home.html', {'title': 'Home', 'page_name':'home'})

def rate_view(request):
    return render(request, 'rate.html', {'title' : 'Rate', 'page_name':'rate'})

def feed_view(request):
    return render(request, 'feed.html', {'title' : 'Feed', 'page_name':'feed'})

def ranking_view(request):
    return render(request, 'ranking.html', {'title' : 'Ranking', 'page_name':'ranking'})

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

def post_view(request, post_id):
    pp_post = get_list_or_404(PredictedImagePost, pk=post_id)
    context = {'title': 'Post #' + str(post_id), 'page_name':'post', 'pp_post':pp_post}
    return render(request, 'post_view.html', context)

def not_found_404(request, exception):
    return render(request, 'not_found_404.html', {'title' : 'Not found...'})