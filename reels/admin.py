from django.contrib import admin
from .models import Reel, ReelLike, ReelComment


@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "caption", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "caption")


@admin.register(ReelLike)
class ReelLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "reel", "created_at")


@admin.register(ReelComment)
class ReelCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "reel", "text", "created_at")
