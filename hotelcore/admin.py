from django.contrib import admin
from .models import Hotel , Room , Reservation

@admin.register(Reservation)

class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "guest_name",
        "room",
        "check_in",
        "check_out",
        "status",
        "total_price",
    )
    list_filter = ('status', 'check_in')
    search_fields = ('guest_name',)
    readonly_fields = ('total_price',)

def formatted_total_price(self, obj):
    return f"{obj.total_price:,.0f}"

formatted_total_price.short_description = "Total Price"
list_display = (..., 'formatted_total_price')