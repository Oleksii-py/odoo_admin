from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Worker, Nationality


class WorkerSerializer(ModelSerializer):
    # user = StringRelatedField(read_only=True)
    class Meta:
        model = Worker
        fields = ["id", "nationality", "gender", "birthday"]


class NationalitySerializer(ModelSerializer):
    class Meta:
        model = Nationality
        fields = "__all__"
