from django.shortcuts import render, redirect
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer
from .permissions import IsOwnerOrAdmin


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
def home(request):
    rooms = Room.objects.all()

    if request.method == "POST":
        guest_name = request.POST.get('guest_name')
        room_id = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        room = Room.objects.get(id=room_id)

        Reservation.objects.create(
            guest_name=guest_name,
            room=room,
            check_in=check_in,
            check_out=check_out
        )

        return redirect('/')

    reservations = Reservation.objects.all().order_by('-id')

    return render(request, 'home.html', {
        'reservations': reservations,
        'rooms': rooms
    })