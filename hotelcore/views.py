from django.shortcuts import render, redirect
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer
from .permissions import IsOwnerOrAdmin
from datetime import datetime

# 🟢 API Views
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'room']
    search_fields = ['guest_name']
    ordering_fields = ['total_price', 'created_at']

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()


# 🟢 Front View (سایت کاربر)
from django.shortcuts import render, redirect
from .models import Room, Reservation


def home(request):

        if request.method == 'POST':

            guest_name = request.POST.get('guest_name')
            room_id = request.POST.get('room')
            guests = request.POST.get('guests')

            check_in = datetime.strptime(
            request.POST.get('check_in'),
            '%Y-%m-%d'
        ).date()

        check_out = datetime.strptime(
            request.POST.get('check_out'),
            '%Y-%m-%d'
        ).date()

        room = Room.objects.get(id=room_id)

        Reservation.objects.create(
            guest_name=guest_name,
            room=room,
            guests=guests,
            check_in=check_in,
            check_out=check_out
        )

        return redirect('/')

        rooms = Room.objects.all()
        reservations = Reservation.objects.all().order_by('-id')

        return render(request, 'home.html', {
        'rooms': rooms,
        'reservations': reservations
    })