import datetime
from django.db.models import Q
from rest_framework import viewsets, permissions, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Message
from .serializer import MessageSerializer, SendMessageSerializer, FullMessageSerializer


class ManageMassagesView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = {'sender': request.user.id}
        data = {**data, **request.data}
        serializer = SendMessageSerializer(data=data)
        print(serializer.is_valid())
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        usr = request.user.id
        path = request.get_full_path()
        if path == '/':
            queryset = Message.objects.filter(
                Q(receiver=usr, receiver_delete=False) | Q(sender=usr, sender_delete=False))
        elif path == '/unread/':
            queryset = Message.objects.filter(receiver=usr, read=False, receiver_delete=False)
        else:
            queryset = None
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read = True
        instance.save()
        serializer = FullMessageSerializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        usr = self.request.user.id
        if instance.sender_delete and instance.receiver_delete:
            instance.delete()
        elif instance.sender.id == usr:
            instance.sender_delete = True
            instance.save()
        elif instance.receiver.id == usr:
            instance.receiver_delete = True
            instance.save()

