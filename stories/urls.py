from django.urls import path
from . import views

urlpatterns = [
    path("", views.stories_view, name="stories"),
    path("create/", views.create_story, name="create-story"),
]
