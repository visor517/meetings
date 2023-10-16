from django.urls import path

from apps.booking.views import *


app_name = "booking"

urlpatterns = [
    path("create/", ReservationCreateView.as_view(), name="create"),
    path("update/<pk>/", ReservationUpdateView.as_view(), name="update"),
    path("delete/<pk>/", ReservationDeleteView.as_view(), name="delete"),
]
