from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.db.models import F
from odoo_admin.permission import IsAdminOrReadOnlyIsAuthenticated
from .serializers import RoomSerializer, AccommodationSerializer
from .models import Room, Accommodation


# Create your views here.
class AccommodationViewSet(ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyIsAuthenticated]


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.select_related("accommodation").all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyIsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name", "accommodation__name"]

    @action(detail=False, methods=["get"])
    def available(self, request):
        qs = self.get_queryset().filter(
            capacity__gt=F("capacity") - F("assignments__count")
        )
        rooms = [r for r in qs if r.available_beds > 0]
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
