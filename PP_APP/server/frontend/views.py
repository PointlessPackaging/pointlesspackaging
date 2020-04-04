from django.shortcuts import render, redirect

# Create your views here.
def about_view(request):
    return render(request, 'frontend/about.html', {'title' : 'About'})

def home_view(request):
    return render(request, 'frontend/home.html', {'title' : 'Home'})

def upload_view(request):
    return render(request, 'frontend/upload.html', {'title' : 'Upload'})
