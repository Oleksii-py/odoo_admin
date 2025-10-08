from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from odoo_admin.permission import RoleModelPermission
from .serializers import WorkerSerializer, NationalitySerializer, WorkerDetailSerializer
from .models import Worker, Nationality


# Create your views here.
class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all().select_related("workposition_id", "nationality_id")
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return WorkerDetailSerializer
        return super().get_serializer_class()


class NationalityViewSet(ModelViewSet):
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [IsAuthenticated, RoleModelPermission]
