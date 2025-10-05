from rest_framework.serializers import ModelSerializer
from .models import WorkPlace, WorkPosition


class WorkPlaceSerializer(ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = ["id", "name", "is_workplace", "address"]


class WorkPositionSerializer(ModelSerializer):
    class Meta:
        model = WorkPosition
        fields = ["id", "name", "workplace"]
