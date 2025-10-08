from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import WorkPlace, WorkPosition


class WorkPositionSerializer(ModelSerializer):
    class Meta:
        model = WorkPosition
        fields = ("id", "name", "is_active")


class WorkPlaceSerializer(ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = ("id", "name", "address")
    

class WorkPlaceAggregationSerializer(ModelSerializer):
    active_positions = SerializerMethodField()

    class Meta:
        model = WorkPlace
        fields = ("id", "name", "address", "active_positions")

    def get_active_positions(self, obj):
        positions = getattr(obj, "active_positions_cache", [])
        return WorkPositionSerializer(positions, many=True).data
