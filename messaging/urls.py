from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("<int:pk>/", views.conversation_detail, name="conversation-detail"),
    path("new/<str:username>/", views.start_conversation, name="start-conversation"),
]
