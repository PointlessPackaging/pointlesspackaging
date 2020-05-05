from django.shortcuts import render, redirect


# Create your views here.
def about_view(request):
    return render(request, 'frontend/about.html', {'title': 'About'})


def home_view(request):
    return render(request, 'frontend/home.html', {'title': 'Home'})


def upload_view(request):
    return render(request, 'frontend/upload.html', {'title': 'Upload'})


def success_view(request):
    return render(request, 'frontend/success.html', {'title': 'Success!'})


def charts_view(request, *args, **kwargs):
    return render(request, 'charts.html', {})


def tables_view(request, *args, **kwargs):
    return render(request, 'tables.html', {})
