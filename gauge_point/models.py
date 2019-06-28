from django.db import models
from user.models import User


class Gauge_Point(models.Model):
    """
    标记点
    """
    # 一个用户产生多个标记点d
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content_text = models.TextField(max_length=1024, null=True, blank=True, verbose_name='文字')
    picture = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name='图片')
    videos = models.FileField(upload_to='video', null=True, blank=True, verbose_name='视频')
    latitude = models.CharField(max_length=32, blank=True, null=True, verbose_name="纬度")
    longitude = models.CharField(max_length=32, blank=True, null=True, verbose_name="经度")
    GAUGE_IN_TYPE_CHOICES = (
        (0, 'text'),
        (1, 'picture'),
        (2, 'videos'),
    )
    gauge_type = models.IntegerField(choices=GAUGE_IN_TYPE_CHOICES, default=0, verbose_name='发布类型')
    transmit = models.BooleanField(default=False, verbose_name='是否转发')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    is_past = models.BooleanField(default=False, verbose_name='是否过期')
    like_num = models.IntegerField(default=0, verbose_name='点赞数量')
    address = models.CharField(max_length=255, null=True, verbose_name='地址')
    labels = models.CharField(max_length=1024, null=True, verbose_name='标签')

    class Meta:
        db_table = 'gauge_point'


class Like_Count(models.Model):
    """
    标记点 点赞
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    gauge_point = models.ForeignKey(Gauge_Point, on_delete=models.CASCADE, verbose_name='标记点')
    like = models.BooleanField(default=False, verbose_name="是否点赞")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        db_table = 'like_count'


class Report(models.Model):
    """
    举报
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    gauge_point = models.OneToOneField(Gauge_Point, on_delete=models.CASCADE, verbose_name='标记点')
    cause = models.CharField(max_length=255, null=True, blank=True, verbose_name='举报原因')
    result = models.CharField(max_length=255, null=True, blank=True, verbose_name='反馈结果')
    REOIRT_STATE = (
        (0, '审核中'),
        (1, '反馈结果'),
    )
    report_state = models.IntegerField(choices=REOIRT_STATE, default=0, verbose_name='审核状态')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    is_del = models.BooleanField(default=False)

    class Meta:
        db_table = 'report'