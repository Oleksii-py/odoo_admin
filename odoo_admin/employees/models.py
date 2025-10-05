from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Worker(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    nationality = models.ForeignKey(
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
    birthday = models.DateField(blank=True, null=True)


class Nationality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=3, unique=True)
    flag_emoji = models.CharField(max_length=4, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Nationalities"
        ordering = ["name"]

    def __str__(self):
        return self.name
