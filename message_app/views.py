from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            usr = serializer.save()
            data['response'] = 'User is registered successfully'
            data['email'] = usr.email
            data['username'] = usr.username
            token = Token.objects.get(user=usr).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
