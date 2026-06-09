from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Reel, ReelLike


@login_required
def reels_feed(request):
    reels = Reel.objects.all().order_by("-created_at")
    return render(request, "reels/reels_feed.html", {"reels": reels})


@login_required
def create_reel(request):
    if request.method == "POST":
        video = request.FILES.get("video")
        caption = request.POST.get("caption", "")
        if video:
            Reel.objects.create(user=request.user, video=video, caption=caption)
            messages.success(request, "Reel uploaded!")
        else:
            messages.error(request, "Video is required.")
        return redirect("reels-feed")
    return redirect("reels-feed")


@login_required
def like_reel(request, pk):
    reel = get_object_or_404(Reel, pk=pk)
    like, created = ReelLike.objects.get_or_create(user=request.user, reel=reel)
    if not created:
        like.delete()
        return JsonResponse({"liked": False, "likes_count": reel.likes.count()})
    return JsonResponse({"liked": True, "likes_count": reel.likes.count()})
