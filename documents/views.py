from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ClientDocumentForm, AdminDocumentForm
from .models import Document

User = get_user_model()


@login_required
def document_list(request):
    user = request.user
    if user.is_admin_role:
        docs = Document.objects.select_related("owner", "uploaded_by").all()
        client_id = request.GET.get("client")
        if client_id:
            docs = docs.filter(owner_id=client_id)
        clients = User.objects.filter(role=User.Role.CLIENT).order_by("username")
        return render(request, "documents/admin_list.html", {"docs": docs, "clients": clients,
                                                                "selected_client": client_id})
    else:
        docs = Document.objects.filter(owner=user)
        return render(request, "documents/client_list.html", {"docs": docs})


@login_required
def client_upload(request):
    if not request.user.is_client:
        raise PermissionDenied
    if request.method == "POST":
        form = ClientDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect("documents:list")
    else:
        form = ClientDocumentForm()
    return render(request, "documents/upload.html", {"form": form})


@login_required
def admin_upload(request):
    if not request.user.is_admin_role:
        raise PermissionDenied
    if request.method == "POST":
        form = AdminDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, "Document sent to client.")
            return redirect("documents:list")
    else:
        form = AdminDocumentForm()
        form.fields["owner"].queryset = User.objects.filter(role=User.Role.CLIENT)
    return render(request, "documents/upload.html", {"form": form})


@login_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if not (request.user.is_admin_role or doc.owner_id == request.user.id):
        raise PermissionDenied
    doc.file.delete(save=False)
    doc.delete()
    messages.info(request, "Document deleted.")
    return redirect("documents:list")
