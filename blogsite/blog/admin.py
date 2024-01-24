from django.contrib import admin
from .models import Post, Comment


# Define admin actions
# Update posts to be published
@admin.action(description="Update posts from Draft to published")
def make_published(modeladmin, request, queryset):
    queryset.update(status=Post.Status.PUBLISHED)


@admin.action(description="Deactivate comments")
def deactivate_comment(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.action(description="Activate comments")
def activate_comment(modeladmin, request, queryset):
    queryset.update(active=True)


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "published", "status"]
    list_filter = ["status", "published", "author", "created"]
    search_fields = ["title", "body"]
    raw_id_fields = ["author"]
    date_hierarchy = "published"
    ordering = ["status", "published"]
    prepopulated_fields = {"slug": ["title"]}

    # register the actions to the modelAdmin
    actions = [make_published]


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = [
        "active",
        "created",
        "updated",
    ]
    search_fields = ["name", "email", "body"]

    actions = [deactivate_comment, activate_comment]
