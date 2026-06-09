from django.urls import path
from . import views

urlpatterns = [
    path("", views.reels_feed, name="reels-feed"),
    path("create/", views.create_reel, name="create-reel"),
    path("<int:pk>/like/", views.like_reel, name="like-reel"),
]
