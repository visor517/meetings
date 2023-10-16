from django.contrib import admin
from django.urls import include, path

from apps.booking.views import ReservationListView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ReservationListView.as_view(), name="index"),
    path("reservations/", include("apps.booking.urls", namespace="reservations")),
    path("users/", include("apps.users.urls", namespace="users")),
]
