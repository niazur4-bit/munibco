from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/password/", views.change_password_view, name="change_password"),
    path("password-reset/", views.MunibPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.MunibPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.MunibPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.MunibPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
