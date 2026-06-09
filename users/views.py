from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Follow
from posts.models import Post, SavedPost


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("feed")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "feed")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    posts = Post.objects.filter(user=user).order_by("-created_at")
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    posts_count = posts.count()

    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    saved_posts = []
    if request.user == user:
        saved_posts = Post.objects.filter(saved_by__user=user).order_by(
            "-saved_by__created_at"
        )

    context = {
        "profile_user": user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count,
        "is_following": is_following,
        "saved_posts": saved_posts,
    }
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "users/edit_profile.html", context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect("user-profile", username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=user_to_follow
    )
    if created:
        from notifications.models import Notification
        Notification.objects.create(
            sender=request.user,
            receiver=user_to_follow,
            notification_type="follow",
        )
        messages.success(request, f"You are now following {username}!")
    else:
        messages.info(request, f"You are already following {username}.")
    return redirect("user-profile", username=username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        follower=request.user, following=user_to_unfollow
    )
    if follow.exists():
        follow.delete()
        messages.success(request, f"You have unfollowed {username}.")
    else:
        messages.info(request, f"You are not following {username}.")
    return redirect("user-profile", username=username)


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = User.objects.filter(following__following=user)
    context = {"title": "Followers", "users_list": followers, "profile_user": user}
    return render(request, "users/user_list.html", context)


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    followings = User.objects.filter(followers__follower=user)
    context = {"title": "Following", "users_list": followings, "profile_user": user}
    return render(request, "users/user_list.html", context)


def search_users(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(is_superuser=True)
    return render(
        request, "users/search_results.html", {"results": results, "query": query}
    )
