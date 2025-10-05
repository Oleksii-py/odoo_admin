from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Accommodation, Room, HousingAssignment


class AccommodationSerializer(ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ["id", "name", "address", "created_at"]


class RoomSerializer(ModelSerializer):
    available_beds = IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = ["id", "accommodation", "name", "capacity", "available_beds"]
