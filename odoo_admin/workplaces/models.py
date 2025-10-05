from django.db import models


# Create your models here.
class WorkPlace(models.Model):
    name = models.CharField(max_length=255)
    is_workplace = models.BooleanField(default=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class WorkPosition(models.Model):
    name = models.CharField(max_length=255)
    workplace = models.ForeignKey(
        WorkPlace, on_delete=models.PROTECT, related_name="positions"
    )

    def __str__(self):
        return f"{self.name} @ {self.workplace.name}"
