from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Choice


@receiver(post_save, sender=Choice)
def choice_post_save(sender, **kwargs):
    question = kwargs['instance'].question
    question.closed_at += timezone.timedelta(days=1)

    question.save()
