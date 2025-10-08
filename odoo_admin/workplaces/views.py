from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from odoo_admin.permission import RoleModelPermission
from .serializers import WorkPlaceSerializer, WorkPositionSerializer, WorkPlaceAggregationSerializer
from .models import WorkPlace, WorkPosition


# Create your views here.
class WorkPlaceViewSet(ModelViewSet):
    queryset = WorkPlace.objects.all()
    serializer_class = WorkPlaceSerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]


class WorkPositionViewSet(ModelViewSet):
    queryset = WorkPosition.objects.select_related("workplace").all()
    serializer_class = WorkPositionSerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]


class AggregationViewSet(APIView):
    permission_classes = [IsAuthenticated, RoleModelPermission]
    model = WorkPlace
    serializer = WorkPlaceAggregationSerializer

    def get(self, request, format=None):
        active_positions_prefetch = Prefetch(
            "workposition_set",
            queryset=WorkPosition.objects.filter(is_active=True),
            to_attr="active_positions_cache"
        )

        workplaces = self.model.objects.prefetch_related(active_positions_prefetch).all()
        return Response(self.serializer(workplaces, many=True).data)