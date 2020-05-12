from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic.list import ListView
from pp_api.models import ImagePost, PredictedImagePost, Packager, PPUsers


# Create your views here.
def home_view(request):
    return render(request, 'home.html', {'title': 'Home', 'page_name': 'home'})


def rate_view(request):
    return render(request, 'rate.html', {'title': 'Rate', 'page_name': 'rate'})


class FeedView(ListView):
    model = PredictedImagePost
    paginate_by = 3
    context_object_name = 'feed'
    template_name = 'feed.html'
    ordering = ['-img_post__date_posted']

    def get_queryset(self):
        query = self.request.GET.get('packager')
        if query:
            bad_chars = [';', ':', '!', '*', '?',''] 
            query=''.join(i for i in query if not i in bad_chars)
            query = query.strip().replace(" ", "").lower()
            object_list = self.model.objects.filter(packager__name__istartswith=query).order_by('-img_post__date_posted')
        else:
            object_list = self.model.objects.all().order_by('-img_post__date_posted')
        return object_list

    def get_context_data(self,**kwargs):
        context = super(FeedView,self).get_context_data(**kwargs)
        query=self.request.GET.get('packager')
        if query:
            bad_chars = [';', ':', '!', '*', '?',''] 
            query=''.join(i for i in query if not i in bad_chars)
            context['packager']=str(query)
            context['search_success']=True
        else:
            context['packager']=None
            context['search_success']=None
        context['title']='Feed'
        context['page_name']='feed'
        return context
    

def ranking_view(request):
    return render(request, 'ranking.html', {'title': 'Ranking', 'page_name': 'ranking'})


def about_view(request):
    return render(request, 'about.html', {'title': 'About', 'page_name': 'about'})


def upload_view(request):
    return render(request, 'upload.html', {'title': 'Upload'})


def success_view(request):
    return render(request, 'success.html', {'title': 'Success!'})


def charts_view(request, *args, **kwargs):
    return render(request, 'charts.html', {'title': 'Charts'})


def tables_view(request, *args, **kwargs):
    return render(request, 'tables.html', {'title': 'Tables'})


def post_view(request, post_id):
    pp_post = get_list_or_404(PredictedImagePost, pk=post_id)
    context = {
        'title': 'Post #' + str(post_id),
        'page_name': 'post',
        'pp_post': pp_post,
        'meta_img': pp_post[0].img_post.infer_img,
    }
    return render(request, 'post.html', context)


def not_found_404(request, exception):
    return render(request, 'not_found_404.html', {'title': 'Not found...'})
