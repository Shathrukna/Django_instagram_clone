from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit-profile"),
    path("profile/<str:username>/", views.profile, name="user-profile"),
    path("follow/<str:username>/", views.follow_user, name="follow-user"),
    path("unfollow/<str:username>/", views.unfollow_user, name="unfollow-user"),
    path(
        "followers/<str:username>/",
        views.followers_list,
        name="followers-list",
    ),
    path(
        "following/<str:username>/",
        views.following_list,
        name="following-list",
    ),
    path("search/", views.search_users, name="search-users"),
]
