from rest_framework.permissions import BasePermission
from .models import Message
from rest_framework.exceptions import PermissionDenied


class ReadPermission(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        if request.method == 'GET':
            msg = Message.objects.get(id=pk)
            user = request.user
            if user == msg.receiver and not msg.receiver_delete:
                msg.read = True
                msg.save()
                return True
            elif user == msg.sender and not msg.sender_delete:
                return True
            else:
                return False
        else:
            return False


class DeletePermission(BasePermission):
    def has_permission(self, request, view):
        self.error = ''
        pk = view.kwargs.get('pk')
        if request.method == "GET":
            msg = Message.objects.get(id=pk)
            user = request.user
            if user == msg.sender:
                if msg.receiver_delete:
                    msg.delete()
                    self.error = "message has been deleted"
                    raise PermissionDenied(self.error)
                else:
                    msg.sender_delete = True
                    msg.save()
                    self.error = "sender deleted the message"
                    raise PermissionDenied(self.error)
            elif user == msg.receiver:
                if msg.sender_delete:
                    msg.delete()
                    self.error = "message has been deleted"
                    raise PermissionDenied(self.error)
                else:
                    msg.receiver_delete = True
                    msg.save()
                    self.error = "receiver deleted the message"
                    raise PermissionDenied(self.error)
            else:
                self.error = "only user who sent or receive can delete"
                raise PermissionDenied(self.error)
        else:
            return False
