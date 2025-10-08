import uuid
from django.db import models

# Create your models here.
class Worker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=64)
    nationality_id = models.ForeignKey(
        "Nationality",
        on_delete=models.PROTECT,
        related_name="workers",
        null=True,
        blank=True,
    )
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    birthday = models.DateField()
    comment = models.CharField(blank=True, null=True)
    document_number = models.CharField(blank=True, null=True)
    validity_document = models.DateField(blank=True, null=True)
    
    workposition_id = models.ForeignKey(
        "workplaces.WorkPosition",
        on_delete=models.PROTECT,
        related_name="workers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Nationality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=3, unique=True)
    flag_emoji = models.CharField(max_length=4, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
