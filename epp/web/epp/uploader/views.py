from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from visionAPI.analyzer import Analyzer
from uploader.forms import UploaderForm
from uploader.models import Uploader

from rest_framework.views import APIView
from rest_framework.response import Response


def home_view(request):
    if request.method == 'POST':
        form = UploaderForm(request.POST, request.FILES)

        saved_image = request.FILES.get('epp_image')
        path = "../media/images/" + str(saved_image)

        analyzer = Analyzer(path)  # google viosn api

        if form.is_valid():
            form.save()
            context = {
                "after_image": path,
                "before_image": path,
                "materials": analyzer.get_materials()
            }
            return render(request, 'home.html', context)
            # return redirect('success')

    context = {'form': UploaderForm(),
               'customers': 10}
    return render(request, "home.html", context)


# Testing 2
# from random import randint
# from django.views.generic import TemplateView
# from chartjs.views.lines import BaseLineChartView
#
#
# class LineChartJSONView(BaseLineChartView):
#     def get_labels(self):
#         """Return 7 labels for the x-axis."""
#         return ["January", "February", "March", "April", "May", "June", "July"]
#
#     def get_providers(self):
#         """Return names of datasets."""
#         return ["Central", "Eastside", "Westside"]
#
#     def get_data(self):
#         """Return 3 datasets to plot."""
#
#         return [[75, 44, 92, 11, 44, 95, 35],
#                 [41, 92, 18, 3, 73, 87, 92],
#                 [87, 21, 94, 3, 90, 13, 65]]
#
#
# line_chart = TemplateView.as_view(template_name='home.html')
# line_chart_json = LineChartJSONView.as_view()

# Testing 3

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)  # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = 5
        # User.objects.all().count()
        labels = ["Amazon", "Walmart", "Ebay", "Target", "Costco", "DoorDash"]
        label_counts = [qs_count, 8, 8, 3, 7, 2]
        data = {
            "labels": labels,
            "default": label_counts,
        }
        # return render(request, "home.html", data)
        return Response(data)


def temp_view(request):
    return render(request, "temp.html", {})


def success_view(request):
    return HttpResponse('successfully uploaded')
