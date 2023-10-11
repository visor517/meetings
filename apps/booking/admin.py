from django.contrib import admin
from .models import Room, Reservation


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    search_fields = list_display


@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    list_display = ["room", "owner", "start_time", "finish_time", "description"]
    list_filter = ["room", "owner", "start_time", "finish_time"]
    save_on_top = True
