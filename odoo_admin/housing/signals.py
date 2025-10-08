from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HousingAssignment
from event.models import HousingAssignmentHistory


@receiver(post_save, sender=HousingAssignment)
def sync_housing_assignment_history(sender, instance, created, **kwargs):
    HousingAssignmentHistory.objects.create(
        worker_id=instance.worker_id,
        room_id=instance.room_id,
        check_in_date=instance.check_in_date,
        check_out_date=instance.check_out_date,
        state=instance.state,
    )