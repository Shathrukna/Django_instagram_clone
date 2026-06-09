from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(receiver=request.user)
    unread_count = notifications.filter(is_read=False).count()
    context = {
        "notifications": notifications,
        "unread_count": unread_count,
    }
    return render(request, "notifications/notifications.html", context)


@login_required
def mark_as_read(request, pk):
    notification = Notification.objects.get(pk=pk, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")


@login_required
def mark_all_read(request):
    Notification.objects.filter(receiver=request.user, is_read=False).update(
        is_read=True
    )
    return redirect("notifications")
