import datetime

from django.core import serializers
from django.db.models import F, Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from dynamictalk.models import DynamicTalk, Report_Friends, Like
from homepage.models import MeetLike
from user.models import UserImg, UserToken, User
from utils.function import get_token, base_image
from utils.status_code import JsonRep
from django.core.paginator import Paginator


# 朋友圈发布
@api_view(['GET', 'POST'])
def issue_friend(request):
    if request.method == 'POST':
        # 获取要上传的数据
        content_text = request.POST.get('content_text', None)
        pictures = request.POST.get('pictures', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        open_type = request.POST.get('open_type', 0)
        address = request.POST.get('address')
        labels = request.POST.get('labels')
        picture_list = [] if len(pictures) == 0 or pictures is None else pictures.split(',')
        if not all([latitude, longitude]) and (not all(pictures) or (
                content_text is None and len(content_text) == 0)):
            return JsonResponse(JsonRep().FAILED(msg='缺少必要参数'))
        user = get_token(request)
        try:
            dynamictalk = DynamicTalk()
            dynamictalk.content_text = content_text
            dynamictalk.user = user
            dynamictalk.latitude = latitude
            dynamictalk.longitude = longitude
            dynamictalk.open_type = open_type
            dynamictalk.address = address
            dynamictalk.labels = labels
            dynamictalk.save()
            for picture in picture_list:
                img = base_image(picture)
                UserImg(user=user, img=img, img_type=3, dynamictalk_id=dynamictalk.id).save()
            cls_dict = {}
            pictures = user.userimg_set.filter(Q(img_type=3) & Q(dynamictalk_id=dynamictalk.id)).all()
            if pictures:
                images = []
                for picture in pictures:
                    images.append(picture.img.name)
                cls_dict['id'] = dynamictalk.id
                cls_dict['user_id'] = dynamictalk.user_id
                cls_dict['content_text'] = dynamictalk.content_text
                cls_dict['images'] = images
                cls_dict['gauge_type'] = dynamictalk.gauge_type
                cls_dict['latitude'] = dynamictalk.latitude
                cls_dict['longitude'] = dynamictalk.longitude
                cls_dict['open_type'] = dynamictalk.open_type
                cls_dict['like_count'] = dynamictalk.like_count
                cls_dict['create_time'] = dynamictalk.create_time.strftime('%F %X')
                cls_dict['address'] = dynamictalk.address
                cls_dict['labels'] = dynamictalk.labels

            return JsonResponse(JsonRep().SUCCESS(msg='发布成功', data=cls_dict))
        except Exception as e:
            print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(code=-2, msg='发布失败'))


@api_view(['GET', 'POST'])
def check_friend(request):
    if request.method == 'POST':
        sereen_type = int(request.POST.get('sereen_type', 0))
        page = request.POST.get('page')
        user = get_token(request)
        dynamictalk = DynamicTalk.objects.all().order_by('-id')
        pg = Paginator(dynamictalk, 10)
        dynamictalk = pg.page(page)
        # json_data = serializers.serialize("json", page, ensure_ascii=False)

        if sereen_type == 1:  # 1：喜欢我的
            like_users = MeetLike.objects.filter(friend_id=user.id)
            likeme_userid = [cls.id for cls in like_users]
            # 查喜欢我的用户动态
            dynamictalk = dynamictalk.filter(user_id__in=likeme_userid)

        elif sereen_type == 2:  # 2：我喜欢的
            user_likes = MeetLike.objects.filter(user=user)
            melike_userid = [cls.user_friend_id for cls in user_likes]
            # 查我喜欢的用户动态
            dynamictalk = dynamictalk.filter(user_id__in=melike_userid)

        elif sereen_type == 3:  # 3:相互喜欢的
            meetlike = user.meetlike_set.all()
            likeme_relationships = meetlike.filter(friend_id=user.id)
            likeme_userid = [cls.id for cls in meetlike]
            melike_relationships = meetlike.filter(user=user)
            melike_userid = [cls.user_friend_id for cls in meetlike]
            ships_userid = likeme_userid or melike_userid
            dynamictalk = dynamictalk.filter(user_id__in=ships_userid)
        else:
            pass
        cls_dict = {}
        result = []
        if dynamictalk:
            # label = DynamicTalk.objects.filter(user_id=user.id).first()
            # cls_dict['labels'] = label.labels
            # cls_dict['page'] = json_data
            for cls in dynamictalk:
                dict = {}
                pictures = UserImg.objects.filter(Q(img_type=3) & Q(dynamictalk_id=cls.id)).all()
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
            cls_dict['result'] = result
            return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=cls_dict,))
        else:
            return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=cls_dict))


@api_view(['GET', 'POST'])
def check_index(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        page = int(request.POST.get('page', 1))
        user_friend = User.objects.filter(pk=friend_id).first()
        user = get_token(request)
        dynamictalk = DynamicTalk.objects.filter(user_id=friend_id).all().order_by('-id')
        dynamictalk_count = dynamictalk.count()
        pg = Paginator(dynamictalk, 10)
        dynamictalk = pg.page(page)
        friend_dict = {}
        result = []
        if dynamictalk:
            label = DynamicTalk.objects.filter(user_id=friend_id).first()
            login_time = UserToken.objects.filter(user_id=friend_id).order_by('-id')
            jl = user.meetnum_set.filter(meetcount=friend_id).first()
            dt = datetime.datetime.now()
            age = dt.year - user_friend.birth.year
            img = user.userimg_set.filter(img_type=1).first()
            friend_dict['img'] = img.img.name
            friend_dict['username'] = user_friend.username
            friend_dict['gender'] = user_friend.gender
            friend_dict['age'] = age
            friend_dict['dynamictalk_count'] = dynamictalk_count
            friend_dict['login_time'] = login_time[0].create_time.strftime('%F %X')
            friend_dict['distance'] = jl.distance
            friend_dict['labels'] = label.labels
            for cls in dynamictalk:
                dict = {}
                pictures = user_friend.userimg_set.filter(Q(img_type=3) & Q(dynamictalk_id=cls.id)).all()
                if pictures:
                    images = []
                    for picture in pictures:
                        images.append(picture.img.name)
                    dict['id'] = cls.id
                    dict['content_text'] = cls.content_text
                    dict['images'] = images
                    dict['create_time'] = cls.create_time.strftime('%F %X')
                    dict['like_count'] = cls.like_count
                    dict['address'] = cls.address
                    result.append(dict)
                else:
                    dict['id'] = cls.id
                    dict['content_text'] = cls.content_text
                    dict['images'] = []
                    dict['create_time'] = cls.create_time.strftime('%F %X')
                    dict['like_count'] = cls.like_count
                    dict['address'] = cls.address
                    result.append(dict)
            friend_dict['result'] = result
            return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=friend_dict))
        else:
            return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=friend_dict))


@api_view(['GET', 'POST'])
def like_friend(request):
    dynamictalk_id = int(request.POST.get('dynamictalk_id', 0))
    like = int(request.POST.get('like', 0))
    user = get_token(request)
    try:
        dynamictalk = DynamicTalk.objects.get(id=dynamictalk_id)
        # 判断点赞记录是否存在，如果存在则不进行点赞，如果不存在则进行点赞数量加一
        if Like.objects.filter(dynamictalk=dynamictalk, like=like, user_id=user.id).exists():
            Like.objects.get(dynamictalk=dynamictalk, like=like, user_id=user.id).delete()
            if dynamictalk.like_count >= 1:
                dynamictalk.like_count = F('like_count') - 1
                dynamictalk.save()
        else:
            Like.objects.create(dynamictalk=dynamictalk, like=like, user_id=user.id)
            dynamictalk.like_count = F('like_count') + 1
            dynamictalk.save()

    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(msg='操作失败'))

    return JsonResponse(JsonRep().SUCCESS(msg='操作成功'))


@api_view(['GET', 'POST'])
def report_friend(request):
    dynamictalk_id = int(request.POST.get('dynamictalk_id', 0))
    cause = request.POST.get('cause', None)
    user = get_token(request)
    try:
        dynamictalk = DynamicTalk.objects.get(pk=dynamictalk_id)
        Report_Friends(user=user, dynamictalk=dynamictalk, cause=cause).save()
        return JsonResponse(JsonRep().SUCCESS(msg='举报成功'))
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(msg='举报失败'))


@api_view(['GET'])
def del_friend(request):
    dynamictalk_id = request.POST.get('dynamictalk_id')
    try:
        dynamictalk = DynamicTalk.objects.get(id=dynamictalk_id)
        dynamictalk.delete()
        return JsonResponse(JsonRep().SUCCESS(msg='删除成功'))
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().SUCCESS(msg='删除失败'))
