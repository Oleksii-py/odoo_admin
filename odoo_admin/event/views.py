from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from odoo_admin.permission import RoleModelPermission
from .serializers import HousingAssignmentHistorySerializer
from .models import HousingAssignmentHistory

# Create your views here.
class EventView(APIView):
    permission_classes = [IsAuthenticated, RoleModelPermission]
    model = HousingAssignmentHistory
    serializer = HousingAssignmentHistorySerializer

    def get(self, request, pk=None, format=None):
        if pk:
            try:
                event = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return Response({"detail": "Not found."}, status=404)
            serializer = self.serializer_class(event)
            return Response(serializer.data)

        events = self.model.objects.all()
        serializer = self.serializer(events, many=True)
        return Response(serializer.data)
    
