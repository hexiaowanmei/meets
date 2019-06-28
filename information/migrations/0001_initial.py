# Generated by Django 2.1 on 2019-06-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_id', models.IntegerField(verbose_name='好友id')),
                ('content', models.TextField(max_length=1024, null=True, verbose_name='文字')),
                ('chat_time', models.DateTimeField(auto_now=True, verbose_name='聊天时间')),
                ('user', models.ManyToManyField(to='user.User', verbose_name='用户')),
            ],
            options={
                'db_table': 'chat',
            },
        ),
    ]
