from django.db import models

# Create your models here.
from django.db import models

from user.models import User


class BackUser(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False, blank=True, verbose_name="姓名")
    password = models.CharField(max_length=255, verbose_name="密码")

    class Meta:
        db_table = 'backuser'


# Create your models here.
# 用户动态
# class DynamicTalk(models.Model):
#     # dynamic_id = models.IntegerField(primary_key=True)
#     # user_id = models.IntegerField(blank=True, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
#     content_text = models.TextField(max_length=1024, null=True, blank=True, verbose_name='文字')
#     picture = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name='图片')
#     # videos = models.FileField(upload_to='video', null=True, blank=True, verbose_name='视频')
#     GAUGE_IN_TYPE_CHOICES = (
#         (0, 'text'),
#         (1, 'picture'),
#         # (2, 'videos'),
#     )
#     gauge_type = models.IntegerField(choices=GAUGE_IN_TYPE_CHOICES, default=0, verbose_name='发布类型')
#     dynamic_addr = models.CharField(max_length=255, blank=True, null=True, verbose_name="动态地址")
#     latitude = models.DecimalField(null=False, max_digits=9, decimal_places=6, verbose_name="纬度")
#     longitude = models.DecimalField(null=False, max_digits=9, decimal_places=6, verbose_name="经度")
#     like = models.BooleanField(default=False, verbose_name='是否点赞')
#     like_count = models.IntegerField(default=0, blank=True, null=True, verbose_name="点赞数")
#     transmit = models.BooleanField(default=False, verbose_name='是否转发')
#     create_time = models.DateTimeField(auto_now=True, verbose_name='发布时间')
#     is_open = models.BooleanField(default=True, verbose_name='是否公开')
#
#     class Meta:
#         db_table = 'dynamic_talk'


