from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    # Annotate each conversation with other_user and unread_count
    conv_data = []
    for conv in conversations:
        other_user = conv.participants.exclude(pk=request.user.pk).first()
        unread_count = conv.messages.filter(is_read=False).exclude(
            sender=request.user
        ).count()
        conv_data.append({
            "conversation": conv,
            "other_user": other_user,
            "unread_count": unread_count,
            "last_message": conv.messages.last(),
        })
    context = {"conv_data": conv_data}
    return render(request, "messaging/inbox.html", context)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation, pk=pk, participants=request.user
    )
    messages_list = Message.objects.filter(conversation=conversation)

    # Mark messages as read
    messages_list.filter(is_read=False).exclude(sender=request.user).update(
        is_read=True
    )

    other_user = conversation.participants.exclude(pk=request.user.pk).first()

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get("text", "")
            image = form.cleaned_data.get("image")
            voice = form.cleaned_data.get("voice")
            msg_kwargs = {
                "conversation": conversation,
                "sender": request.user,
            }
            if text:
                msg_kwargs["text"] = text
            if image:
                msg_kwargs["image"] = image
            if voice:
                msg_kwargs["voice"] = voice
            Message.objects.create(**msg_kwargs)
            return redirect("conversation-detail", pk=conversation.pk)
    else:
        form = MessageForm()

    conversations = Conversation.objects.filter(participants=request.user)
    conv_data = []
    for conv in conversations:
        other = conv.participants.exclude(pk=request.user.pk).first()
        unread = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        conv_data.append({
            "conversation": conv,
            "other_user": other,
            "unread_count": unread,
            "last_message": conv.messages.last(),
        })

    context = {
        "conversation": conversation,
        "messages": messages_list,
        "form": form,
        "other_user": other_user,
        "conv_data": conv_data,
    }
    return render(request, "messaging/chat.html", context)


@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        django_messages.error(request, "You cannot message yourself.")
        return redirect("profile")

    # Find existing conversation
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect("conversation-detail", pk=conversation.pk)
