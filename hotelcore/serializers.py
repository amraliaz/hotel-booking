from rest_framework import serializers
from django.db.models import Q
from .models import Hotel, Room, Reservation


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    room = RoomSerializer(read_only=True)

    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True
    )

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        room = data.get('room')

        if check_out <= check_in:
            raise serializers.ValidationError({
                "check_out": "Check-out must be after check-in."
            })

        queryset = Reservation.objects.filter(room=room)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        ).exists():
            raise serializers.ValidationError({
                "room": "This room is already booked for these dates."
            })

        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = f"{float(data['total_price']):,.0f}"