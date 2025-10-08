from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Worker, Nationality
from housing.serializers import RoomSerializer
from workplaces.serializers import WorkPositionSerializer



class WorkerSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class NationalitySerializer(ModelSerializer):
    class Meta:
        model = Nationality
        fields = "__all__"


class WorkerDetailSerializer(ModelSerializer):
    workposition = WorkPositionSerializer(read_only=True, source="workposition_id")
    nationality = NationalitySerializer(read_only=True, source="nationality_id")
    room = SerializerMethodField()

    class Meta:
        model = Worker
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "nationality",
            "gender",
            "birthday",
            "comment",
            "document_number",
            "validity_document",
            "workposition",
            "room",
        ]

    def get_room(self, obj):
        assignment = obj.housing_assignments.filter(state="active").first()
        if assignment:
            return {
                "id": assignment.room_id.id,
                "name": assignment.room_id.name,
                "accommodation": assignment.room_id.accommodation_id.name,
            }
        return None



