from apps.booking.models import Reservation


def check_intervals(form, pk=None):
    """ Проверяем свободен ли выбранный интервал """
    data = form.cleaned_data

    if exist_intervals := Reservation.objects.exclude(pk=pk).filter(
                start_time__date=data["start_time"].date(),
                room_id=data["room"].id).order_by("start_time"
            ).values("start_time", "finish_time"):

        for interval in exist_intervals:
            if data["finish_time"] <= interval["start_time"]:
                break
            if data["start_time"] < interval["finish_time"]:
                form.add_error(None, "Указанное время попадает в занятый интервал")
                break
    return form
