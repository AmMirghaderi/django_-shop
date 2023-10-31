from celery import shared_task
from datetime import timedelta, datetime
from .models import OtpCode


@shared_task
def remove_expired_code():
    expired_time = datetime.now() - timedelta(minutes=1)
    OtpCode.objects.filter(created__lt=expired_time).delete()
