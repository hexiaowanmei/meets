from django.db import models
from user.models import User


class DynamicTalk(models.Model):
    """
    用户动态
    """
    # dynamic_id = models.IntegerField(primary_key=True)
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content_text = models.TextField(max_length=1024, null=True, blank=True, verbose_name='文字')
    picture = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name='图片')
    # videos = models.FileField(upload_to='video', null=True, blank=True, verbose_name='视频')
    GAUGE_IN_TYPE_CHOICES = (
        (0, 'text'),
        (1, 'picture'),
        # (2, 'videos'),
    )
    gauge_type = models.IntegerField(choices=GAUGE_IN_TYPE_CHOICES, default=0, verbose_name='发布类型')
    latitude = models.DecimalField(null=False, max_digits=9, decimal_places=6, verbose_name="纬度")
    longitude = models.DecimalField(null=False, max_digits=9, decimal_places=6, verbose_name="经度")
    OPEN_TYPE = (
        ('0', '公开'),
        ('1', '喜欢我的'),
        ('2', '我喜欢的'),
        ('3', '相互喜欢'),
    )
    open_type = models.IntegerField(choices=OPEN_TYPE, default=0, verbose_name='公开类型')
    like_count = models.IntegerField(default=0, blank=True, null=True, verbose_name="点赞数")
    transmit = models.BooleanField(default=False, verbose_name='是否转发')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    address = models.CharField(max_length=255, null=True, verbose_name='地址')
    labels = models.CharField(max_length=1024, null=True, verbose_name='标签')

    class Meta:
        db_table = 'dynamic_talk'


class Like(models.Model):
    """
    朋友圈 点赞
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    dynamictalk = models.ForeignKey(DynamicTalk, on_delete=models.CASCADE, verbose_name='用户动态')
    like = models.BooleanField(default=False, verbose_name="是否点赞")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        db_table = 'like'


class Report_Friends(models.Model):
    """
    朋友圈举报
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    dynamictalk = models.OneToOneField(DynamicTalk, on_delete=models.CASCADE, verbose_name='用户动态')
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
        db_table = 'report_friends'