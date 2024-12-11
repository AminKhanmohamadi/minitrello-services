import string
import uuid
import random
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from trello.apps.users.sender import send_otp


# Create your models here.
class User(AbstractUser):
    pass


class OtpRequestQuerySet(models.QuerySet):
    def is_valid(self , reciver , request , password):
        current_time = timezone.now()
        return self.filter(
            reciver=reciver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),
        ).exists()


class OTPManager(models.Manager):
    def get_queryset(self):
        return OtpRequestQuerySet(self.model, using=self._db)

    def is_valid(self , reciver , request , password):
        return self.get_queryset().is_valid(reciver , request , password)

    def generate(self , data):
        otp = self.model(channel=data['channel'], reciver=data['reciver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp


def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits , k=4)
    return ''.join(digits)

class OTPRequest(models.Model):
    class OtpChannel(models.TextChoices):
        PHONE = 'Phone'
        EMAIL = 'E-Mail'

    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.CharField(max_length=10, choices=OtpChannel.choices, default=OtpChannel.PHONE)
    reciver = models.CharField(max_length=50)
    password = models.CharField(max_length=4 , default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()