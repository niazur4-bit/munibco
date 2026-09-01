from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Max
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MessageForm
from .models import Message

User = get_user_model()


def _admin_user():
    return User.objects.filter(role=User.Role.ADMIN).first() or User.objects.filter(is_superuser=True).first()


@login_required
def inbox(request):
    user = request.user
    if user.is_admin_role:
        client_ids = Message.objects.filter(Q(sender__role=User.Role.CLIENT) | Q(recipient__role=User.Role.CLIENT)) \
            .values_list("sender", "recipient")
        ids = set()
        for a, b in client_ids:
            ids.add(a)
            ids.add(b)
        clients = User.objects.filter(id__in=ids, role=User.Role.CLIENT)
        # also include all clients so admin can start a new thread
        all_clients = User.objects.filter(role=User.Role.CLIENT).order_by("username")
        threads = []
        for c in all_clients:
            last = Message.objects.filter(Q(sender=c, recipient=user) | Q(sender=user, recipient=c)).order_by("-timestamp").first()
            unread = Message.objects.filter(sender=c, recipient=user, is_read=False).count()
            threads.append({"client": c, "last": last, "unread": unread})
        threads.sort(key=lambda t: t["last"].timestamp if t["last"] else t["client"].date_joined, reverse=True)
        return render(request, "chatapp/admin_inbox.html", {"threads": threads})
    else:
        admin_user = _admin_user()
        if not admin_user:
            return render(request, "chatapp/no_admin.html")
        return redirect("chatapp:thread", user_id=admin_user.id)


@login_required
def thread(request, user_id):
    other = get_object_or_404(User, pk=user_id)
    user = request.user
    # permission: client can only message admin; admin can message any client
    if user.is_client and not other.is_admin_role:
        raise PermissionDenied
    if user.is_admin_role and not other.is_client and other.id != user.id:
        raise PermissionDenied

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid() and (form.cleaned_data.get("body") or form.cleaned_data.get("attachment")):
            msg = form.save(commit=False)
            msg.sender = user
            msg.recipient = other
            msg.save()
            return redirect("chatapp:thread", user_id=other.id)
    else:
        form = MessageForm()

    Message.objects.filter(sender=other, recipient=user, is_read=False).update(is_read=True)
    msgs = Message.objects.filter(Q(sender=user, recipient=other) | Q(sender=other, recipient=user)).order_by("timestamp")
    return render(request, "chatapp/thread.html", {"other": other, "messages_list": msgs, "form": form})
