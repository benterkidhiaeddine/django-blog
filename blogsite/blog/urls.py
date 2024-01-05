from django.urls import path
from .views import post_detail, PostList, post_share

# Define the application namespace to separate the urls of this application from others
app_name = "blog"
urlpatterns = [
    path("posts/", view=PostList.as_view(), name="post_list"),
    path(
        "posts/<int:year>/<int:month>/<int:day>/<slug:post>/",
        view=post_detail,
        name="post_detail",
    ),
    path("posts/<int:post_id>/share/", view=post_share, name="post_share"),
]
