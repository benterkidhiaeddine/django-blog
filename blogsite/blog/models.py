from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Define Custom Managers
class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Define Custom Managers
class DraftManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.DRAFT)


# Create your models here.
class Post(models.Model):
    # Define a status for the Post
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        # This is used inside queries Applied at the User model
        related_query_name="blog_post",
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, unique_for_date="published")
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    # Add the default manager and the custom managers
    objects = models.Manager()  # Default manager
    published_posts = PublishedManager()
    draft_posts = DraftManager()

    class Meta:
        ordering = ["-published"]

        indexes = [models.Index(fields=["-published"], name="published_date_desc")]

    def __str__(self) -> str:
        return f"title:{self.title}"

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.published.year,
                self.published.month,
                self.published.day,
                self.slug,
            ],
        )

    def get_share_absolute_url(self):
        return reverse("blog:post_share", args=[self.pk])


# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # Name of the user who left the comment
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"
