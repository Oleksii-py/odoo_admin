from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from odoo_admin.permission import IsAdminOrReadOnlyIsAuthenticated
from .serializers import WorkPlaceSerializer, WorkPositionSerializer
from .models import WorkPlace, WorkPosition


# Create your views here.
class WorkPlaceViewSet(ModelViewSet):
    queryset = WorkPlace.objects.all()
    serializer_class = WorkPlaceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyIsAuthenticated]


class WorkPositionViewSet(ModelViewSet):
    queryset = WorkPosition.objects.select_related("workplace").all()
    serializer_class = WorkPositionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyIsAuthenticated]
