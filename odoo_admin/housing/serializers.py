from rest_framework.serializers import ModelSerializer, IntegerField, ValidationError
from .models import Accommodation, Room, HousingAssignment


class AccommodationSerializer(ModelSerializer):
    class Meta:
        model = Accommodation
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    available_beds = IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class HousingAssignmentSerializer(ModelSerializer):
    class Meta:
        model = HousingAssignment
        fields = "__all__"
        read_only_fields = ['state','created_at','updated_at']

    def validate(self, attrs):
        worker = attrs.get('worker_id')
        room = attrs.get('room_id')
        if self.instance is None:
            if room.available_beds <= 0:
                raise ValidationError("No available beds in this room.")
            if HousingAssignment.objects.filter(worker_id=worker, state='active').exists():
                raise ValidationError("This worker already has an active housing assignment.")
        return attrs
