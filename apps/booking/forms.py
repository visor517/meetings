from django import forms

from apps.booking.models import Reservation, Room


class ReservationForm(forms.ModelForm):
    owner_id = forms.IntegerField(widget=forms.HiddenInput())
    start_time = forms.DateTimeField(
        label="Начало",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control", "step": 300}),
        )
    finish_time = forms.DateTimeField(
        label="Окончание",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control", "step": 300}),
        )

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        start_time = cleaned_data.get("start_time")
        finish_time = cleaned_data.get("finish_time")
        if start_time and finish_time and start_time >= finish_time:
            self.add_error(None, "Окончание должно быть больше начала")
        if start_time.date() != finish_time.date():
            self.add_error(None, "Даты должны совпадать")

        if not self.errors:
            # проверяем на свободность
            if exist_intervals := Reservation.objects.exclude(id=cleaned_data.get("id")).filter(
                        start_time__date=start_time.date(),
                        room_id=room.id).order_by("start_time"
                    ).values("start_time", "finish_time"):

                for interval in exist_intervals:
                    if finish_time <= interval["start_time"]:
                        break
                    if start_time < interval["finish_time"]:
                        self.add_error(None, "Указанное время попадает в занятый интервал")
                        break

        return cleaned_data

    class Meta:
        model = Reservation
        fields = "__all__"
        exclude = ["owner"]


class ReservationUpdateForm(ReservationForm):
    start_time = forms.DateTimeField(
        label="Начало",
        widget=forms.DateTimeInput(attrs={"type": "text", "class": "form-control"}),
    )
    finish_time = forms.DateTimeField(
        label="Окончание",
        widget=forms.DateTimeInput(attrs={"type": "text", "class": "form-control"}),
    )


class TimeTableForm(forms.Form):
    room_id = forms.ChoiceField(
        label="Название комнаты",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=[(room.id, room.name) for room in Room.objects.all()],
    )
    table_day = forms.DateField(
        label="День",
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
