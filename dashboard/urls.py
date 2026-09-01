from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.redirect_dashboard, name="redirect"),
    path("client/", views.client_dashboard, name="client_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/records/", views.record_list, name="record_list"),
    path("admin/records/new/", views.record_create, name="record_create"),
]
