import uuid

from django.db import models

# Create your models here.
class HousingAssignmentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATE_CHOICES = [
        ("active", "Active"),
        ("past", "Past"),
    ]
    worker_id = models.ForeignKey(
        "employees.Worker", on_delete=models.SET_NULL, blank=True, null=True, related_name="housing_assignments_history"
    )
    room_id = models.ForeignKey("housing.Room", on_delete=models.SET_NULL, blank=True, null=True, related_name="assignments_history")
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)