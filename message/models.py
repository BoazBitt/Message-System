from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="received_messages")
    subject = models.CharField(max_length=50)
    msg = models.TextField()
    creation_date = models.DateField(auto_now=True)
    read = models.BooleanField(default=False)
    sender_delete = models.BooleanField(default=False)
    receiver_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.subject + ' ' + str(self.creation_date)

# class MessageManager(models.Model):


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=False, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        print(Token.objects.get(user=instance))
