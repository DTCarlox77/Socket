from django.urls import path
from .views import main

urlpatterns = [
    path('chats/<str:sala>/', main, name='main'),
]