from django.db import models


class User(models.Model):
    """
    用户表
    """
    # user_id = models.IntegerField(primary_key=True)
    code_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='ID')
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户名')
    mobile = models.CharField(max_length=32, blank=True, null=True, verbose_name='手机号')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='密码')
    birth = models.DateField(blank=True, null=True, verbose_name='出生日期')
    GENDER_CHOICES = (
        (0, "男"),
        (1, "女"),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    CONSTELLATION_CHOICES = (
        (1, "白羊座"),
        (2, "金牛座"),
        (3, "双子座"),
        (4, "巨蟹座"),
        (5, "狮子座"),
        (6, "处女座"),
        (7, "天秤座"),
        (8, "天蝎座"),
        (9, "射手座"),
        (10, "摩羯座"),
        (11, "水瓶座"),
        (12, "双鱼座"),
    )
    constellation = models.IntegerField(choices=CONSTELLATION_CHOICES, blank=True, null=True, verbose_name='星座')
    # 用户对账号修改判断，True可以修改，flase不可以修改
    is_alter = models.BooleanField(default=False, verbose_name='是否修改')
    scope = models.CharField(max_length=124, verbose_name="地区")
    signature = models.CharField(max_length=255, blank=True, null=True, verbose_name='个性签名')
    latitude = models.DecimalField(null=False, max_digits=9, decimal_places=6, verbose_name="纬度")
    longitude = models.DecimalField(null=False, max_digits=9, decimal_places=6, verbose_name="经度")

    class Meta:
        db_table = 'user'


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        db_table = 'user_token'


class UserImg(models.Model):
    """
    用户图片
    """
    # img_id = models.IntegerField(primary_key=True)
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    # gauge_point = models.ForeignKey('gauge_point.Gauge_Point', null=True, on_delete=models.CASCADE, verbose_name="标记点")
    dynamictalk = models.ForeignKey('dynamictalk.DynamicTalk', null=True, on_delete=models.CASCADE, verbose_name='动态')
    img = models.ImageField(upload_to='upload', blank=True, null=True, verbose_name="照片")
    is_first = models.IntegerField(blank=True, null=True, verbose_name="是否首张")
    default_display = models.IntegerField(blank=True, null=True, verbose_name="默认展示")
    IMG_TYPE_CHOICES = (
        (1, "头像"),
        (2, "相册"),
        (3, "说说"),
    )
    img_type = models.IntegerField(choices=IMG_TYPE_CHOICES, blank=True, null=True, verbose_name="图片类型")

    class Meta:
        db_table = 'user_img'


class Lable(models.Model):
    """
    标签
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    LABLE_CHOICES = (
        (1, '运动'),
        (2, '游戏'),
        (3, '摄影'),
        (4, '金融'),
        (5, '汽车'),
        (6, '房产'),
        (7, '旅游'),
        (8, '家居'),
        (9, '穿搭'),
        (10, '美食'),
        (11, '生活'),
        (12, '商务'),
        (13, '美容'),
        (14, '科技'),
        (15, '休闲'),
        (16, '教育'),
        (17, '政法'),
        (18, '养生'),
    )
    lable = models.IntegerField(choices=LABLE_CHOICES, verbose_name='标签')

    class Meta:
        db_table = 'lable'


# 用户反馈
class Feedback(models.Model):
    """
      用户反馈表
    """
    # feedback_id = models.IntegerField(primary_key=True)
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    centent = models.TextField(blank=True, null=True, verbose_name="反馈内容")
    centent_type = models.CharField(max_length=20, blank=True, null=True, verbose_name="反馈类型")

    class Meta:
        db_table = 'feedback'


class Relationships(models.Model):
    """
    用户关系
    """
    # relationship_id = models.IntegerField(primary_key=True)
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    ship_id = models.IntegerField(blank=True, null=True, verbose_name="被关注用户ID")
    is_friends = models.BooleanField(default=False, verbose_name="是否互关")

    class Meta:
        db_table = 'relationships'


class UserSettings(models.Model):
    """
    用户设置
    """
    # setting_id = models.IntegerField(primary_key=True)
    # user_id = models.IntegerField(blank=True, null=True, verbose_name="用户")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    start_time = models.CharField(max_length=10, blank=True, null=True, verbose_name="免打扰开始时间")
    end_time = models.CharField(max_length=10, blank=True, null=True, verbose_name="免打扰结束时间")
    inform_method = models.CharField(max_length=30, blank=True, null=True, verbose_name="消息通知")
    hint_method = models.CharField(max_length=30, blank=True, null=True, verbose_name="提示方式")

    class Meta:
        db_table = 'user_settings'

