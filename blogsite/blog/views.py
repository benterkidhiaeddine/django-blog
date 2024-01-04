from datetime import date


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post

# Create your views here.


def post_list(request):
    published_posts = Post.published_posts.all()

    page_number = request.GET.get("page", 1)
    posts_paginator = Paginator(published_posts, 3)

    posts = posts_paginator.get_page(page_number)

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
