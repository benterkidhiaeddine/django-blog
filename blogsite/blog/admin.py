from django.contrib import admin
from .models import Post


# Define admin actions
@admin.action(description="Update posts from Draft to published")
def make_published(modeladmin, request, queryset):
    queryset.update(status=Post.Status.PUBLISHED)


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
