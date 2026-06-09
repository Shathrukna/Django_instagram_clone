from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("feed")
    return redirect("login")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_redirect, name="root"),
    path("", include("users.urls")),
    path("posts/", include("posts.urls")),
    path("notifications/", include("notifications.urls")),
    path("messages/", include("messaging.urls")),
    path("stories/", include("stories.urls")),
    path("reels/", include("reels.urls")),
]

# Serve media files
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
