from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from apps.booking.models import Reservation, Room
from apps.booking.forms import ReservationForm


class ReservationListView(ListView):
    model = Reservation
    template_name = "timetable.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            "rooms": Room.objects.all(),
            "add_form": ReservationForm,
            "room": Room.objects.get(id=self.request.GET.get("room-id", 1))
        })
        return context

    def get_queryset(self):
        room_id = self.request.GET.get("room-id", 1)

        try:
            return Reservation.objects.filter(room_id=room_id)
        except ObjectDoesNotExist:
            return None


class ReservationView(CreateView):
    form_class = ReservationForm
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            reservation = Reservation.objects.create(**data)
            print()

        return HttpResponseRedirect(reverse('index'))
