from rest_framework.viewsets import ModelViewSet
from odoo_admin.permission import IsAdminOrReadOnlyIsAuthenticated
from .serializers import WorkerSerializer, NationalitySerializer
from .models import Worker, Nationality


# Create your views here.
class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAdminOrReadOnlyIsAuthenticated]


class NationalityViewSet(ModelViewSet):
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [IsAdminOrReadOnlyIsAuthenticated]
