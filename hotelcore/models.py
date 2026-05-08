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
    class Room(models.Model):
        hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    price_per_night = models.DecimalField(max_digits=12, decimal_places=2)
    capacity = models.IntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.id} - {self.price_per_night}"
class Reservation(models.Model):
    from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from decimal import Decimal
from django.contrib.auth.models import User

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    guest_name = models.CharField(max_length=100)

    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=9)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_nights(self):
        return (self.check_out - self.check_in).days

    def clean(self):
        if not self.room:
            return

        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")

        if not self.room.is_active:
            raise ValidationError("This room is not available.")

        overlapping = Reservation.objects.filter(
            room=self.room
        ).filter(
            Q(check_in__lt=self.check_out) &
            Q(check_out__gt=self.check_in)
        )

        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This room is already booked for these dates.")

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.room:
            nights = self.get_nights()
            base_price = nights * self.room.price_per_night

            discount_amount = base_price * (self.discount_percent / Decimal("100"))
            price_after_discount = base_price - discount_amount

            tax_amount = price_after_discount * (self.tax_percent / Decimal("100"))

            self.total_price = price_after_discount + tax_amount

        super().save(*args, **kwargs)

    def formatted_total_price(self):
        return f"{self.total_price:,.0f}" if self.total_price else "0"

    formatted_total_price.short_description = "Total Price"

    def __str__(self):
         return f"Room {self.number}"

    class Meta:
        ordering = ["-created_at"]