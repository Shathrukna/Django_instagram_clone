from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
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


@login_required
def story_viewer_data(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        followed = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()
        if not followed and request.user != user:
            return JsonResponse({"error": "Not following"}, status=403)
    stories = Story.objects.filter(
        user=user, expires_at__gt=timezone.now()
    ).order_by("-created_at")
    data = [{
        "id": s.id,
        "image_url": s.image.url,
        "caption": s.caption,
        "created_at": s.created_at.isoformat(),
    } for s in stories]
    return JsonResponse({"username": username, "avatar_url": user.profile.image.url, "stories": data})
