from django.contrib import admin

from users.models import User


@admin.register(User)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_staff", "is_active"]
    search_fields = ["username", "email"]
    list_filter = ["is_staff", "is_active"]
