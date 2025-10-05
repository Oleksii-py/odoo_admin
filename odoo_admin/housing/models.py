from datetime import timezone

from django.db import models
from django.contrib.auth import get_user_model

from employees.models import Worker

User = get_user_model()


# Create your models here.
class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    # manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_accommodations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    accommodation = models.ForeignKey(
        Accommodation, on_delete=models.PROTECT, related_name="rooms"
    )
    name = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("accommodation", "name")

    def __str__(self):
        return f"{self.accommodation.name} / {self.name}"

    @property
    def occupied_beds(self):
        qs = self.assignments.filter(state="active")
        return qs.count()

    @property
    def available_beds(self):
        return max(self.capacity - self.occupied_beds, 0)


class HousingAssignment(models.Model):
    STATE_CHOICES = [
        ("active", "Active"),
        ("past", "Past"),
    ]
    worker = models.ForeignKey(
        Worker, on_delete=models.PROTECT, related_name="housing_assignments"
    )
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="assignments")
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-check_in_date"]

    def __str__(self):
        return f"{self.worker} -> {self.room} ({self.check_in_date} - {self.check_out_date or '...'})"

    def mark_checked_out(self, out_date=None):
        if out_date is None:
            out_date = timezone.now().date()
        self.check_out_date = out_date
        self.state = "past"
        self.save()
