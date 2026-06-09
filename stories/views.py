from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Story
from users.models import Follow


@login_required
def stories_view(request):
    followed_users = Follow.objects.filter(
        follower=request.user
    ).values_list("following", flat=True)

    stories = Story.objects.filter(
        user__in=followed_users,
        expires_at__gt=timezone.now(),
    ).select_related("user").order_by("-created_at")

    user_stories = Story.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now(),
    )

    context = {
        "stories": stories,
        "user_stories": user_stories,
    }
    return render(request, "stories/stories.html", context)


@login_required
def create_story(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption", "")
        if image:
            Story.objects.create(user=request.user, image=image, caption=caption)
            messages.success(request, "Story created!")
        else:
            messages.error(request, "Image is required.")
        return redirect("stories")
    return redirect("stories")
