from django.urls import path

from apps.booking.views import *


app_name = "booking"

urlpatterns = [
    path("reservation/", ReservationView.as_view(), name="reservation"),
]
