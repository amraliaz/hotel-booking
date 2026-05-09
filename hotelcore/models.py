from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from decimal import Decimal
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    stars = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} - {self.price_per_night}"


class Reservation(models.Model):
    guest_name = models.CharField(max_length=100)

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    guests = models.IntegerField()

    check_in = models.DateField()
    check_out = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.guest_name