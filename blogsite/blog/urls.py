from django.urls import path
from .views import post_list, post_detail

# Define the application namespace to separate the urls of this application from others
app_name = "blog"
urlpatterns = [
    path("posts/", view=post_list, name="post_list"),
    path(
        "posts/<int:year>/<int:month>/<int:day>/<slug:post>/",
        view=post_detail,
        name="post_detail",
    ),
]
