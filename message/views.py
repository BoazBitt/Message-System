import datetime
from django.db.models import Q, QuerySet
from rest_framework import viewsets, permissions, status
from functools import reduce

from rest_framework.authtoken.admin import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Message, MessageManager
from .serializer import MessageSerializer, SendMessageSerializer, FullMessageSerializer


class ManageMassagesView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = {'sender': request.user.id}
        data = {**data, **request.data}
        read = request.data['receiver']
        users = User.objects.all()
        manager = MessageManager.objects.create()
        for user in users:
            if user.id == request.user.id:
                manager.receivers_delete.add(user)
            if user.id in read:
                manager.receivers_delete.add(user)
                manager.readMessages.add(user)
        data['manager'] = manager.id
        serializer = SendMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        usr = request.user.id
        path = request.get_full_path()
        if path == '/':
            queryset_send = Message.objects.filter(sender=usr, manager__receivers_delete__id=usr)
            queryset_recived = Message.objects.filter(receiver__id=usr, manager__receivers_delete__id=usr)
            queryset = queryset_send.union(queryset_recived)
            print(queryset_send)
            print()
            # queryset = Message.objects.filter(
            #     Q(receiver=usr, receiver_delete=False) | Q(sender=usr, sender_delete=False))
        elif path == '/unread/':
            queryset = Message.objects.filter(receiver__id=usr, manager__readMessages__id=usr,
                                              manager__receivers_delete__id=usr)
            # queryset = Message.objects.filter(receiver=usr, read=False, receiver_delete=False)
        else:
            queryset = None
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        print("in retrive!!!")
        instance = self.get_object()
        # instance.read = True
        print(instance.manager.readMessages.all())
        instance.manager.readMessages.remove(request.user)
        print(instance.manager.readMessages.all())
        print("after retrive!!!")
        serializer = FullMessageSerializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        usr = self.request.user
        if usr in instance.manager.receivers_delete.all():
            instance.manager.receivers_delete.remove(usr)
            instance.manager.save()
        if len(instance.manager.receivers_delete.all()) == 0:
            instance.manager.delete()
            instance.delete()
