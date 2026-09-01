from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.document_list, name="list"),
    path("upload/", views.client_upload, name="client_upload"),
    path("send/", views.admin_upload, name="admin_upload"),
    path("<int:pk>/delete/", views.document_delete, name="delete"),
]
