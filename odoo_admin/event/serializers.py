from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import HousingAssignmentHistory


class HousingAssignmentHistorySerializer(ModelSerializer):
    worker = SerializerMethodField()
    room = SerializerMethodField()

    class Meta:
        model = HousingAssignmentHistory
        fields = [
            "id",
            "worker",
            "room",
            "check_in_date",
            "check_out_date",
            "state",
            "created_at",
            "updated_at",
        ]

    def get_worker(self, obj):
        worker = obj.worker_id
        if not worker:
            return None
        return {
            "id": worker.id,
            "name": worker.name,
            "email": worker.email,
            "phone": worker.phone,
        }

    def get_room(self, obj):
        room = obj.room_id
        if not room:
            return None
        return {
            "id": room.id,
            "name": room.name,
            "accommodation": room.accommodation_id.name,
        }
