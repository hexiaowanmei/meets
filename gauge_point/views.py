import base64
from io import BytesIO

from PIL import Image
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
import math
import datetime

from django.db.models import F, Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from gauge_point.models import Like_Count, Gauge_Point, Report
from user.models import UserImg, User
from utils.function import get_User, get_end_by_dt_7, base_image, get_token
from utils.status_code import JsonRep

# 发布标记点
@api_view(['GET', 'POST'])
def issue_gauge(request):
    if request.method == 'POST':
        content_text = request.POST.get('content_text', None)
        # 多个文件上传 图片、视频
        pictures = request.FILES.getlist('pictures', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        address = request.POST.get('address')
        labels = request.POST.get('labels')
        pictures = [] if (pictures is None or len(pictures) == 0) else (
            pictures if isinstance(pictures, list) else [pictures])
        if not all([latitude, longitude]) and (not all(pictures) or (
                content_text is None and len(content_text) == 0)):
            return JsonResponse(JsonRep().FAILED(msg='缺少必要参数'))
        try:
            user = get_token(request)
            dt = datetime.datetime.now()
            today_gauge_point_set_count = user.gauge_point_set.filter(create_time__year=dt.year,
                                                                      create_time__month=dt.month,
                                                                      create_time__day=dt.day).count()
            if today_gauge_point_set_count > 5:
                return JsonResponse(JsonRep().FAILED(code=-2, msg='一天只能发布5条'))
            gauge_point = Gauge_Point()
            gauge_point.content_text = content_text
            gauge_point.user = user
            gauge_point.latitude = latitude
            gauge_point.longitude = longitude
            gauge_point.address = address
            gauge_point.labels = labels
            gauge_point.save()
            for picture in pictures:
                img = base_image(picture)
                UserImg(user=user, img=img, img_type=3, gauge_point_id=gauge_point.id).save()
            cls_dict = {}
            pictures = user.userimg_set.filter(Q(img_type=3) & Q(gauge_point_id=gauge_point.id)).all()
            if pictures:
                images = []
                for picture in pictures:
                    images.append(picture.img.name)
                cls_dict['id'] = gauge_point.id
                cls_dict['user_id'] = gauge_point.user_id
                cls_dict['content_text'] = gauge_point.content_text
                cls_dict['images'] = images
                cls_dict['gauge_type'] = gauge_point.gauge_type
                cls_dict['latitude'] = gauge_point.latitude
                cls_dict['longitude'] = gauge_point.longitude
                cls_dict['like_num'] = gauge_point.like_num
                cls_dict['create_time'] = gauge_point.create_time.strftime('%F %X')
                cls_dict['address'] = gauge_point.address
                cls_dict['labels'] = gauge_point.labels
            return JsonResponse(JsonRep().SUCCESS(msg='发布成功', data=cls_dict))
        except Exception as e:
            print(e)
            return JsonResponse(JsonRep().FAILED(code=-3, msg='发布失败'))


@api_view(['GET', 'POST'])
def check_gauge(request):
    # 查看标记点
    if request.method == 'GET':
        create_time = request.GET.get('create_time', 'desc')
        like_num = request.GET.get('like_num', 'desc')
        page = request.POST.get('page')
        user = get_token(request)
        # 只查看最近7天的记录
        dt = datetime.datetime.now()
        old_dt = get_end_by_dt_7(dt)
        # desc降序
        create_time = '-create_time' if create_time == 'desc' else 'create_time'
        like_num = '-like_num' if like_num == 'desc' else 'like_num'
        gauge_point = Gauge_Point.objects.filter(create_time__lte=dt,
                                                 create_time__gte=old_dt).order_by(create_time).order_by(like_num)
        pg = Paginator(gauge_point, 10)
        gauge_point = pg.page(page)

        gauge_point_dict = {}
        result = []
        if gauge_point:
            for cls in gauge_point:
                dict = {}
                pictures = UserImg.objects.filter(Q(img_type=3) & Q(gauge_point_id=cls.id)).all()
                if pictures:
                    images = []
                    for picture in pictures:
                        images.append(picture.img.name)
                    img = UserImg.objects.filter(img_type=1).first()

                    dict['img'] = img.img.name
                    dict['username'] = User.objects.get(id=cls.user_id).username
                    dict['id'] = cls.id
                    dict['user_id'] = cls.user_id
                    dict['content_text'] = cls.content_text
                    dict['images'] = images
                    dict['gauge_type'] = cls.gauge_type
                    dict['latitude'] = cls.latitude
                    dict['longitude'] = cls.longitude
                    dict['open_type'] = cls.open_type
                    dict['like_count'] = cls.like_count
                    dict['create_time'] = cls.create_time.strftime('%F %X')
                    dict['address'] = cls.address
                    dict['labels'] = cls.labels
                    result.append(dict)
                else:
                    img = user.userimg_set.filter(img_type=1).first()

                    dict['img'] = img.img.name
                    dict['username'] = User.objects.get(id=cls.user_id).username
                    dict['id'] = cls.id
                    dict['user_id'] = cls.user_id
                    dict['content_text'] = cls.content_text
                    dict['images'] = []
                    dict['gauge_type'] = cls.gauge_type
                    dict['latitude'] = cls.latitude
                    dict['longitude'] = cls.longitude
                    dict['open_type'] = cls.open_type
                    dict['like_count'] = cls.like_count
                    dict['create_time'] = cls.create_time.strftime('%F %X')
                    dict['address'] = cls.address
                    dict['labels'] = cls.labels
                    result.append(dict)
            gauge_point_dict['result'] = result
            return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=gauge_point_dict))
        else:
            return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=gauge_point_dict))


# 点赞
@api_view(['GET'])
def like_gauge(request):
    gauge_point_id = int(request.GET.get('gauge_point_id', 0))
    like = int(request.GET.get('like', 0))
    user = get_token(request)
    try:
        gauge_point = Gauge_Point.objects.get(pk=gauge_point_id)
        # 判断点赞记录是否存在，如果存在则不进行点赞，如果不存在则进行点赞数量加一
        if Like_Count.objects.filter(gauge_point=gauge_point, like=like, user_id=user.id).exists():
            # 存在则进行取消点赞,删除点赞记录
            Like_Count.objects.get(gauge_point=gauge_point, like=like, user_id=user.id).delete()
            if gauge_point.like_num >= 1:
                gauge_point.like_num = F('like_num') - 1
                gauge_point.save()
        else:
            # 进行点赞，即实例化一个点赞记录
            Like_Count.objects.create(gauge_point=gauge_point, like=like, user_id=user.id)
            gauge_point.like_num = F('like_num') + 1
            gauge_point.save()
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(msg='操作失败'))

    return JsonResponse(JsonRep().SUCCESS(msg='操作成功'))


@api_view(['GET'])
def del_gauge(request):
    gauge_point_id = request.POST.get('gauge_point_id')
    try:
        gauge_point = Gauge_Point.objects.get(id=gauge_point_id)
        gauge_point.delete()
        return JsonResponse(JsonRep().SUCCESS(msg='删除成功'))
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().SUCCESS(msg='删除失败'))


# 标记点举报
@api_view(['GET'])
def report_gauge(request):
    # 得到GET中的数据以及当前用户
    gauge_point_id = int(request.GET.get('gauge_point_id', 0))
    cause = request.GET.get('cause', None)
    user = get_User(request)
    try:
        gauge_point = Gauge_Point.objects.get(pk=gauge_point_id)
        Report(user=user, gauge_point=gauge_point, cause=cause).save()
        return JsonResponse(JsonRep().SUCCESS(msg='举报成功'))
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(msg='举报失败'))