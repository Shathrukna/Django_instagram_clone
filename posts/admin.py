from django.contrib import admin
from .models import Post, Like, Comment, SavedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "caption", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "caption")
    date_hierarchy = "created_at"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "text")


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
