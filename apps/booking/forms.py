from django import forms

from apps.booking.models import Reservation


class ReservationForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        "type": "datetime-local", "class": "form-control"}))
    finish_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        "type": "datetime-local", "class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Введите описание"}))

    class Meta:
        model = Reservation
        fields = "__all__"
