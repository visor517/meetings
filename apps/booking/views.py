from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from apps.booking.models import Reservation, Room
from apps.booking.forms import ReservationForm, TimeTableForm


class ReservationListView(ListView):
    model = Reservation
    template_name = "timetable.html"

    def get_context_data(self, *args, **kwargs):
        params = self.request.GET
        if not (table_day := params.get("table_day")):
            table_day = date.today().strftime("%Y-%m-%d")

        room_id = params.get("room_id", 1)
        room = Room.objects.get(id=room_id)

        context = super().get_context_data(*args, **kwargs)
        context.update({
            "time_table_form": TimeTableForm(initial={
                "room_id": room.id,
                "table_day": table_day}),
            "add_form": ReservationForm,
            "room": room,
        })
        return context

    def get_queryset(self):
        params = self.request.GET

        if not (table_day := params.get("table_day")):
            table_day = date.today().strftime("%Y-%m-%d")
        room_id = params.get("room_id", 1)

        try:
            return Reservation.objects.filter(room_id=room_id, start_time__date=table_day)
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
