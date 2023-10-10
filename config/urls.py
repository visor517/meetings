from django.contrib import admin
from django.urls import path

from booking.views import ReservationListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ReservationListView.as_view(), name="index"),
]
