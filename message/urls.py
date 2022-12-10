from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include
from . import views


router = DefaultRouter()
router.register('read', views.ManageMassagesView, basename='read')
router.register('delete', views.ManageMassagesView, basename='delete')
router.register('unread', views.ManageMassagesView, basename='Unread_messages')
router.register('send', views.ManageMassagesView, basename='send_message')
router.register('', views.ManageMassagesView, basename='all_messages')

urlpatterns = [
    path('', include(router.urls)),

]
