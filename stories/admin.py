from django.contrib import admin
from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("user", "caption", "created_at", "expires_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "caption")
