from django.db import models

# Create your models here.
from user.models import User


class Chat(models.Model):
    user = models.ManyToManyField(User, verbose_name='用户')
    friend_id = models.IntegerField(verbose_name='好友id')
    content = models.TextField(max_length=1024, null=True, verbose_name='文字')
    chat_time = models.DateTimeField(auto_now=True, verbose_name='聊天时间')

    class Meta:
        db_table = 'chat'
