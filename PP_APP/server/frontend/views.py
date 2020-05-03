from django.shortcuts import render, redirect


def home_view(request):
    return render(request, 'index.html', {})


def charts_view(request, *args, **kwargs):
    return render(request, 'charts.html', {})
