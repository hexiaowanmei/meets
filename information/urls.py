from django.urls import path
from information import views


urlpatterns = [
    path('msg_info/', views.msg_info, name='msg_info'),
    path('chat_info/', views.chat_info, name='chat_info'),
]