from django.db import models

from apps.users.models import User


class Room(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Название")
    description = models.CharField(max_length=1023, unique=True, blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return self.name


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations", verbose_name="Комната")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Зарезервировал")
    start_time = models.DateTimeField(db_index=True, verbose_name="Время начала")
    finish_time = models.DateTimeField(verbose_name="Время окончания")
    description = models.CharField(max_length=1023, blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.room.name}: {self.start_time}-{self.finish_time}"
