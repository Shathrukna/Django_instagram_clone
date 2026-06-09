from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications_list, name="notifications"),
    path("mark-read/<int:pk>/", views.mark_as_read, name="mark-notification-read"),
    path("mark-all-read/", views.mark_all_read, name="mark-all-read"),
]
