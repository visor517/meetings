from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.users.views import *

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(redirect_authenticated_user=True, next_page="index"), name="login"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
