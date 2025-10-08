from datetime import datetime

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.db.models import Count, F, Q
from django.db import transaction
from odoo_admin.permission import RoleModelPermission
from .serializers import RoomSerializer, AccommodationSerializer, HousingAssignmentSerializer
from .models import Room, Accommodation, HousingAssignment

# Create your views here.
class AccommodationViewSet(ModelViewSet):
    serializer_class = AccommodationSerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and not user.is_superuser:
            return Accommodation.objects.filter(manager_id=user.id)
        return Accommodation.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(manager_id=user)


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]
    filter_backends = [SearchFilter]
    search_fields = ["name", "accommodation__name"]

    def get_queryset(self):
        user = self.request.user
        qs = Room.objects.select_related("accommodation_id").all()

        if user.is_authenticated and not user.is_superuser:
            qs = qs.filter(accommodation_id__manager_id=user.id)
        return qs

    @action(detail=False, methods=["get"])
    def available(self, request):
        qs = (
            self.get_queryset()
            .annotate(
                active_assignments=Count(
                    "assignments",
                    filter=Q(assignments__state="active"),
                    distinct=True
                )
            )
            .filter(active_assignments__lt=F("capacity"))
        )
        return Response(self.get_serializer(qs, many=True).data)
    

class HousingAssignmentViewSet(ModelViewSet):
    queryset = HousingAssignment.objects.select_related('worker_id','room_id','room_id__accommodation_id').all()
    serializer_class = HousingAssignmentSerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        assignment = self.get_object()
        if assignment.state != 'active':
            return Response({'detail':'Already checked-out.'}, status=400)
        out_date = request.data.get('check_out_date')
        if out_date:
            out_date = datetime.strptime(out_date, '%Y-%m-%d').date()
        assignment.mark_checked_out(out_date)
        return Response(self.get_serializer(assignment).data)

    @action(detail=False, methods=['get'])
    def calendar_events(self, request):
        events = []
        for a in self.get_queryset():
            events.append({
                'id': a.id,
                'title': f"{a.worker_id} → {a.room_id}",
                'start': a.check_in_date.isoformat(),
                'end': (a.check_out_date or a.check_in_date).isoformat(),
                'state': a.state
            })
        return Response(events)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        worker = serializer.validated_data['worker_id']
        room = serializer.validated_data['room_id']
        check_in_date = serializer.validated_data['check_in_date']

        with transaction.atomic():
            room = Room.objects.select_for_update().get(pk=room.pk)
            if room.available_beds <= 0:
                raise ValidationError("No available beds in this room (concurrent check).")
            
            assignment = HousingAssignment.objects.create(
                worker_id=worker,
                room_id=room,
                check_in_date=check_in_date
            )
        
        return Response(self.get_serializer(assignment).data, status=status.HTTP_201_CREATED)
