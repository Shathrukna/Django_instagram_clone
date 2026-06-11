from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Like, Comment, SavedPost
from .forms import PostForm, CommentForm
from users.models import Follow
from notifications.models import Notification


@login_required
def feed(request):
    followed_users = Follow.objects.filter(
        follower=request.user
    ).values_list("following", flat=True)
    posts = Post.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    ).distinct().order_by("-created_at")

    paginator = Paginator(posts, 9)
    page = request.GET.get("page", 1)
    posts_page = paginator.get_page(page)

    comment_form = CommentForm()

    liked_posts = set(
        Like.objects.filter(user=request.user).values_list("post_id", flat=True)
    )
    saved_posts = set(
        SavedPost.objects.filter(user=request.user).values_list("post_id", flat=True)
    )

    from stories.models import Story
    from django.utils import timezone
    import json
    story_users = Follow.objects.filter(
        follower=request.user
    ).values_list("following", flat=True)
    stories = Story.objects.filter(
        user__in=story_users, expires_at__gt=timezone.now()
    ).select_related("user").order_by("-created_at")

    stories_data = []
    seen_users = set()
    for s in stories:
        if s.user.id not in seen_users:
            seen_users.add(s.user.id)
            user_stories = stories.filter(user=s.user)
            stories_data.append({
                "user": s.user,
                "story_ids": json.dumps([st.id for st in user_stories]),
            })

    context = {
        "posts": posts_page,
        "comment_form": comment_form,
        "liked_posts": liked_posts,
        "saved_posts": saved_posts,
        "stories_data": stories_data,
    }
    return render(request, "posts/feed.html", context)


@login_required
def explore(request):
    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 12)
    page = request.GET.get("page", 1)
    posts_page = paginator.get_page(page)
    return render(request, "posts/explore.html", {"posts": posts_page})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been created!")
            return redirect("feed")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by("created_at")
    is_liked = Like.objects.filter(user=request.user, post=post).exists()
    is_saved = SavedPost.objects.filter(user=request.user, post=post).exists()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            if post.user != request.user:
                Notification.objects.create(
                    sender=request.user,
                    receiver=post.user,
                    notification_type="comment",
                    post=post,
                )
            return redirect("post-detail", pk=post.pk)
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "is_liked": is_liked,
        "is_saved": is_saved,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        messages.error(request, "You can't edit this post.")
        return redirect("feed")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated!")
            return redirect("post-detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/create_post.html", {"form": form, "editing": True})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        messages.error(request, "You can't delete this post.")
        return redirect("feed")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("profile")
    return render(request, "posts/post_confirm_delete.html", {"post": post})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        if post.user != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.user,
                notification_type="like",
                post=post,
            )
        return JsonResponse({"liked": True, "likes_count": post.likes.count()})
    else:
        like.delete()
        return JsonResponse({"liked": False, "likes_count": post.likes.count()})
    return redirect(request.META.get("HTTP_REFERER", "feed"))


@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        saved.delete()
        return JsonResponse({"saved": False})
    return JsonResponse({"saved": True})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        messages.error(request, "You can't delete this comment.")
        return redirect(request.META.get("HTTP_REFERER", "feed"))
    post_pk = comment.post.pk
    comment.delete()
    return redirect("post-detail", pk=post_pk)


def context_processors(request):
    return {}
