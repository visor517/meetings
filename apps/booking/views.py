from django.shortcuts import render
from django.views.generic import ListView

from .models import Reservation, Room


class ReservationListView(ListView):
    model = Reservation
    template_name = "timetable.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            "rooms": Room.objects.all(),
        })
        return context
