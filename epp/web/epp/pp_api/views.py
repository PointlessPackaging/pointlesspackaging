from django.shortcuts import render
from django.views.generic import ListView
from pp_api.models import Post
from django.contrib.auth.models import User

posts = Post.objects.all()


def home_view(request):
    return render(request, "pp_api/home.html", {})


class PostListView(ListView):
    model = Post
    template_name = 'pp_api/charts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


def about_view(request):
    context = {
        'posts': posts,
        'title': 'About'
    }
    return render(request, "pp_api/about.html", context)


#TODO: fix the UI of charts.html page
def demo_view(request):
    context = {
        'posts': posts,
        'title': 'Demo'
    }
    return render(request, "pp_api/charts.html", context)


def contact_view(request):
    context = {
        'posts': posts,
        'title': 'Demo'
    }
    return render(request, "pp_api/contact.html", context)

# Some useful functions for DB query:
# complete_set = User.objects.all()
# sub_set = User.objects.filer(username='Kenny')
# user = subset.first() or User.objects.get(id=1)
# user.id or user.pk --> 1
# user.pk --> 1
# user.post_set.all()
# user.post_set.create(top_image='top.png',side_image='side.png')
