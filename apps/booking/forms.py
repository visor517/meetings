from django import forms

from apps.booking.models import Reservation, Room


class ReservationForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local", "class": "form-control"}))
    finish_time = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={"type": "datetime-local", "class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Введите описание"}))

    class Meta:
        model = Reservation
        fields = "__all__"


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
