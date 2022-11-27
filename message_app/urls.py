"""message_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from message import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', obtain_auth_token, name='login'),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),



]
