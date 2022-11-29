import datetime
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Message
from .serializer import MessageSerializer, SendMessageSerializer, FullMessageSerializer
from .custompermission import ReadPermission,DeletePermission


class ReadView(viewsets.ModelViewSet):
    serializer_class = FullMessageSerializer
    permission_classes = [ReadPermission]
    queryset = Message.objects.all()
    http_method_names = ['get']


class DeleteView(viewsets.ModelViewSet):
    serializer_class = FullMessageSerializer
    permission_classes = [DeletePermission]
    queryset = Message.objects.all()
    http_method_names = ['get']

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


class AllMessagesView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(Q(receiver=user,receiver_delete=False) | Q(sender=user,sender_delete=False))
        return queryset


class UnreadMessagesView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(receiver=user, read=False,receiver_delete=False)
        return queryset


class SendMessagesView(viewsets.ModelViewSet):
    serializer_class = SendMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def create(self, data):
        msg = Message.objects.create(
            sender=self.request.user,
            receiver=User.objects.get(id=data.data['receiver']),
            subject=data.data['subject'],
            msg=data.data['msg'],
            creation_date=datetime.date.today()
        )
        msg.save()
        serializer = MessageSerializer(msg)
        return Response(serializer.data)
