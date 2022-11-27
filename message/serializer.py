from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'subject',
            'creation_date',
        ]


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'receiver',
            'subject',
            'msg',
            'creation_date',
        ]


class FullMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'subject',
            'msg',
            'creation_date',
        ]
