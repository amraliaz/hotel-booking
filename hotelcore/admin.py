from django.contrib import admin
from .models import Room, Reservation


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'price_per_night', 'capacity', 'is_active']
    list_filter = ['is_active']
    search_fields = ['room_number']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'guest_name',
        'room',
        'check_in',
        'check_out',
        'guests'
    ]

    search_fields = [
        'guest_name',
        'room__room_number'
    ]