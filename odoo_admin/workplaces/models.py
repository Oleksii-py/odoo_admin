import uuid

from django.db import models

# Create your models here.
class WorkPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_workplace = models.BooleanField(default=True)
    address = models.TextField(blank=True)
    manager_id = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="manager")

    def __str__(self):
        return self.name


class WorkPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    workplace_id = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
