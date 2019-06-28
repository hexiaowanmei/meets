# Generated by Django 2.1 on 2019-06-28 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gauge_Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_text', models.TextField(blank=True, max_length=1024, null=True, verbose_name='文字')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='upload', verbose_name='图片')),
                ('videos', models.FileField(blank=True, null=True, upload_to='video', verbose_name='视频')),
                ('latitude', models.CharField(blank=True, max_length=32, null=True, verbose_name='纬度')),
                ('longitude', models.CharField(blank=True, max_length=32, null=True, verbose_name='经度')),
                ('gauge_type', models.IntegerField(choices=[(0, 'text'), (1, 'picture'), (2, 'videos')], default=0, verbose_name='发布类型')),
                ('transmit', models.BooleanField(default=False, verbose_name='是否转发')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('is_past', models.BooleanField(default=False, verbose_name='是否过期')),
                ('like_num', models.IntegerField(default=0, verbose_name='点赞数量')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='地址')),
                ('labels', models.CharField(max_length=1024, null=True, verbose_name='标签')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'db_table': 'gauge_point',
            },
        ),
        migrations.CreateModel(
            name='Like_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='是否点赞')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
                ('gauge_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gauge_point.Gauge_Point', verbose_name='标记点')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'db_table': 'like_count',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause', models.CharField(blank=True, max_length=255, null=True, verbose_name='举报原因')),
                ('result', models.CharField(blank=True, max_length=255, null=True, verbose_name='反馈结果')),
                ('report_state', models.IntegerField(choices=[(0, '审核中'), (1, '反馈结果')], default=0, verbose_name='审核状态')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_del', models.BooleanField(default=False)),
                ('gauge_point', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gauge_point.Gauge_Point', verbose_name='标记点')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'db_table': 'report',
            },
        ),
    ]
