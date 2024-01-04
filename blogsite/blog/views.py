from datetime import date


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post


# Create your views here


# Create a class based View for post list
class PostList(ListView):
    queryset = Post.published_posts.all()
    context_object_name = "posts"
    template_name = "blog/post/list.html"
    paginate_by = 3


##Keep the function based view for educational purposes , The class based view implement all of this under the hood
def post_list(request):
    published_posts = Post.published_posts.all()

    page_number = request.GET.get("page")
    print(page_number)
    posts_paginator = Paginator(published_posts, 3)

    try:
        posts = posts_paginator.page(page_number)
    except PageNotAnInteger:
        posts = posts_paginator.page(1)
    except EmptyPage:
        # If Specified page is out of the paginator range , return latest page
        posts = posts_paginator.page(posts_paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        published__year=year,
        published__month=month,
        published__day=day,
        slug=post,
    )

    return render(request, "blog/post/detail.html", {"post": post})
