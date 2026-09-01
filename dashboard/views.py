from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404

from documents.models import Document
from chatapp.models import Message
from .models import ServiceRecord
from .forms import ServiceRecordForm
from . import analytics

User = get_user_model()


@login_required
def redirect_dashboard(request):
    if request.user.is_admin_role:
        return redirect("dashboard:admin_dashboard")
    return redirect("dashboard:client_dashboard")


@login_required
def client_dashboard(request):
    if not request.user.is_client:
        return redirect("dashboard:admin_dashboard")
    user = request.user
    records = ServiceRecord.objects.filter(client=user)
    total_spend = records.aggregate(Sum("amount"))["amount__sum"] or 0
    docs_count = Document.objects.filter(owner=user).count()
    unread = Message.objects.filter(recipient=user, is_read=False).count()

    context = {
        "records": records,
        "total_spend": total_spend,
        "docs_count": docs_count,
        "unread": unread,
        "pending_count": records.filter(status="pending").count(),
        "completed_count": records.filter(status="completed").count(),
        "scatter3d": analytics.client_service_scatter3d(records),
        "status_pie": analytics.status_breakdown_3d_pie_like(records),
    }
    return render(request, "dashboard/client_dashboard.html", context)


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role:
        raise PermissionDenied
    records = ServiceRecord.objects.select_related("client").all()
    clients = User.objects.filter(role=User.Role.CLIENT)
    total_revenue = records.aggregate(Sum("amount"))["amount__sum"] or 0
    pending_docs = Document.objects.count()
    unread = Message.objects.filter(recipient=request.user, is_read=False).count()

    context = {
        "clients_count": clients.count(),
        "records_count": records.count(),
        "total_revenue": total_revenue,
        "pending_docs": pending_docs,
        "unread": unread,
        "recent_records": records.order_by("-created_at")[:8],
        "revenue_bar3d": analytics.revenue_by_service_3d_bar(records),
        "trend_surface3d": analytics.monthly_trend_surface(records),
        "status_pie": analytics.status_breakdown_3d_pie_like(records),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def record_list(request):
    if not request.user.is_admin_role:
        raise PermissionDenied
    records = ServiceRecord.objects.select_related("client").all()
    return render(request, "dashboard/record_list.html", {"records": records})


@login_required
def record_create(request):
    if not request.user.is_admin_role:
        raise PermissionDenied
    if request.method == "POST":
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.created_by = request.user
            rec.save()
            return redirect("dashboard:record_list")
    else:
        form = ServiceRecordForm()
        form.fields["client"].queryset = User.objects.filter(role=User.Role.CLIENT)
    return render(request, "dashboard/record_form.html", {"form": form})
