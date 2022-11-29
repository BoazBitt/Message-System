from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include
from . import views


router = DefaultRouter()
router.register('read', views.ReadView, basename='read')
router.register('delete', views.DeleteView, basename='delete')
router.register('unread', views.UnreadMessagesView, basename='Unread_messages')
router.register('send', views.SendMessagesView, basename='send_message')
router.register('', views.AllMessagesView, basename='all_messages')

urlpatterns = [
    path('', include(router.urls)),

]
