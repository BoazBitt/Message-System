# Generated by Django 4.1.3 on 2022-12-10 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0002_remove_message_read_remove_message_receiver_delete_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='manager',
        ),
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='receiver_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.DeleteModel(
            name='MessageManager',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
