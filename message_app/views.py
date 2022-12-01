from django.template.defaulttags import url
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view

from .serializers import RegisterSerializer


class RegisterView(APIView):

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


