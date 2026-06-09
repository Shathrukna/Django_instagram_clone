from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("explore/", views.explore, name="explore"),
    path("create/", views.create_post, name="create-post"),
    path("<int:pk>/", views.post_detail, name="post-detail"),
    path("<int:pk>/edit/", views.edit_post, name="edit-post"),
    path("<int:pk>/delete/", views.delete_post, name="delete-post"),
    path("<int:pk>/like/", views.like_post, name="like-post"),
    path("<int:pk>/save/", views.save_post, name="save-post"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete-comment"),
]
