from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.booking.models import Reservation, Room
from apps.booking.forms import ReservationForm, ReservationUpdateForm, TimeTableForm
from apps.booking.utils import check_intervals

class ReservationListView(ListView):
    model = Reservation
    template_name = "timetable.html"

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        params = self.request.GET
        if not (table_day := params.get("table_day")):
            table_day = date.today().strftime("%Y-%m-%d")

        room_id = params.get("room_id", 1)
        try:
            room = Room.objects.get(id=room_id)
        except ObjectDoesNotExist:
            room = None

        context = super().get_context_data(*args, **kwargs)
        context.update({
            "time_table_form": TimeTableForm(initial={
                "room_id": room_id,
                "table_day": table_day}),
            "add_form": ReservationForm(initial={
                "room": room,
                "owner_id": user.id,
            }),
            "room": room,
        })
        return context

    def get_queryset(self):
        params = self.request.GET

        if not (table_day := params.get("table_day")):
            table_day = date.today().strftime("%Y-%m-%d")
        room_id = params.get("room_id", 1)

        try:
            return Reservation.objects.filter(room_id=room_id, start_time__date=table_day).order_by("start_time")
        except ObjectDoesNotExist:
            return None


class ReservationCreateView(CreateView):
    form_class = ReservationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form = check_intervals(form)
            if not form.errors:
                data = form.cleaned_data
                reservation = Reservation.objects.create(**data)
                url = f"{reverse_lazy('index')}?room_id={reservation.room_id}&table_day={reservation.start_time.date()}"
                return JsonResponse({"success": True, "message": url})

        return JsonResponse({"success": False, "message": str(form.errors).replace("errorlist", "")})


class ReservationUpdateView(UpdateView):
    form_class = ReservationUpdateForm
    model = Reservation
    template_name = "reservations/update_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = context["reservation"]
        context["form"].initial["owner_id"] = reservation.owner_id
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        instance = self.get_object()

        if form.is_valid():
            form = check_intervals(form, instance.pk)
            if not form.errors:
                data = form.cleaned_data
                reservation = form.save(commit=False)
                reservation.id = instance.id
                reservation.owner_id = data['owner_id']
                reservation.save()
                url = f"{reverse_lazy('index')}?room_id={reservation.room_id}&table_day={reservation.start_time.date()}"
                return JsonResponse({"success": True, "message": url})

        return JsonResponse({"success": False, "message": str(form.errors).replace("errorlist", "")})


class ReservationDeleteView(DeleteView):
    model = Reservation
    success_url = reverse_lazy("index")
