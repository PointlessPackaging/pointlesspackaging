from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


def home_view(request):
    return render(request, 'index.html', {})


def charts_view(request, *args, **kwargs):
    return render(request, 'charts.html', {})