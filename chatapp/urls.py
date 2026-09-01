from django.urls import path
from . import views

app_name = "chatapp"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("thread/<int:user_id>/", views.thread, name="thread"),
]
