from django.shortcuts import render, redirect

# Create your views here.
def home_view(request):
    return render(request, 'frontend/home.html', {})
