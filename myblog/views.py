from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from myblog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.


class PostListView(ListView):
    '''
    Post list view -- class achieve
    '''
    queryset = Post.published.all()
    context_object_name = 'posts' #default object_list
    paginate_by = 3
    template_name = 'myblog/post/list.html' #default blog/post_list.html


def post_list(request):
    '''
    Post list view, Show all published posts
    '''
    #All posts shown on one page:
    #posts = Post.published.all()

    #Split the list to pages
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #3 posts for 1 page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "myblog/post/list.html", {'page': page,'posts': posts})

def post_detail(request, year, month, day, post):
    '''
    post detail view
    '''
    post = get_object_or_404(Post,
                            slug = post,
                            status = 'published',
                            publish__year = year,
                            publish__month = month,
                            publish__day = day
                            )
    return render(request, "myblog/post/detail.html", {'post':post})
