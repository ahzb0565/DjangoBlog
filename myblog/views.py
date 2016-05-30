from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from myblog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from myblog.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.


class PostListView(ListView):
    '''
    Post list view -- class achieve
    '''
    queryset = Post.published.all()
    context_object_name = 'posts' #default object_list
    paginate_by = 3
    template_name = 'myblog/post/list.html' #default blog/post_list.html


def post_list(request, tag_slug = None):
    '''
    Post list view, Show all published posts
    '''
    #All posts shown on one page:
    #posts = Post.published.all()
    tag = None
    if tag_slug:
        #Search by tag
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = Post.tags.all(tags__in = [tag])

    else:
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
    return render(request, "myblog/post/list.html", {'page': page,'posts': posts, 'tag': tag})

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
    #list of active comments for this post
    comments = post.comments.filter(active = True)

    if request.method == "POST":
        #A comments was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit = False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        #get empty form
        comment_form = CommentForm()

    return render(request, "myblog/post/detail.html",
        {'post':post, 'comments': comments, 'comment_form':comment_form})

def post_share(request, post_id):
    '''
    share a post by email
    '''
    #Retrieve post by id
    post = get_object_or_404(Post, id= post_id, status = 'published')
    sent = False
    if request.method == "POST":
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form fields pass validation
            cd = form.cleaned_data
            #send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                        cd.get('name'), cd.get('email'), post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                        post.title, post_url, cd.get('name'), cd.get('comments'))
            send_mail(subject, message, 'admin@myblog.com', [cd.get('to')])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'myblog/post/share.html', {'post': post, 'form': form, 'sent':sent})

