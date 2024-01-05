from datetime import date


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    Sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Access the cleaned data
            cd = form.cleaned_data
            # Build the absolute url to give it as a link so the user can click on it : it basically appends  the protocol ( same as request) and the
            # the domain name of server
            post_absolute_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you see Post :{post.title}"
            message = f"Here is the link to this interesting post {post_absolute_url}, \
                {cd['name']} comments are : {cd['comment']}"
            send_mail(
                subject,
                message,
                "benterki.dhiaeddine@gmail.com",
                [cd["to"]],
            )
            Sent = True

            # send the post url via email

    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": Sent}
    )
