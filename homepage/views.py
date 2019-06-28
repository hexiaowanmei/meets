import datetime
from django.db.models import Q
from homepage.models import *
from user.models import User, UserImg
from django.http import JsonResponse
from homepage.redisgeo import *
from utils.function import get_token, fn_timer
from django.views.decorators.cache import cache_page

'遇见主页'

@fn_timer
def homepage(request):
    if request.method == 'POST':
        data = {}
        result_list = []
        user = get_token(request)
        user_friend_num = user.meetnum_set.all()
        if user_friend_num:
            friend_lists = user.meetnum_set.order_by('-id')
            for friend_list in friend_lists:
                user_friend_id = friend_list.meetcount
                '获取朋友的封面图'
                img = AddPhoto.objects.filter(user_id=user_friend_id).first()
                photo = img.image1.name
                user_friend = User.objects.filter(id=user_friend_id).first()
                # friend_photo = Phono.objects.filter(user_id=user_friend_id).first()
                meet_count = user.meetsite_set.filter(friend_id=user_friend_id).first()
                if meet_count:
                    result_dict = {}
                    result_dict['user_id'] = user_friend_id
                    result_dict['gender'] = friend_list.gender
                    result_dict['age'] = friend_list.age
                    result_dict['distance'] = friend_list.distance
                    result_dict['username'] = user_friend.username
                    result_dict['meettime'] = friend_list.meettime
                    result_dict['friend_photo'] = photo
                    result_dict['meet_count'] = meet_count.nums
                    result_list.append(result_dict)
                else:
                    result_dict = {}
                    result_dict['user_id'] = user_friend_id
                    result_dict['gender'] = friend_list.gender
                    result_dict['age'] = friend_list.age
                    result_dict['distance'] = friend_list.distance
                    result_dict['username'] = user_friend.username
                    result_dict['meettime'] = friend_list.meettime
                    result_dict['friend_photo'] = photo
                    result_dict['meet_count'] = 0
                    result_list.append(result_dict)
            user_address = locatebyLatLng(str(user.latitude), str(user.longitude))
            sum_count = Count.objects.filter(user_id=user.id).first()
            sum_count = sum_count.count
            data['sum_count'] = sum_count
            data['result'] = result_list
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
        else:
            return JsonResponse({'code': 201, 'msg': '先去遇见人吧'})


'用户登录过后，判断是否添加过封面图'


def index_image(request):
    if request.method == 'POST':
        user = get_token(request)
        imgs = user.addphoto_set.all()
        if imgs:
            dict_img = {}
            img_list = []
            for img in imgs:
                img = img.image.name
                img_list.append(img)
            dict_img['image'] = img_list
            return JsonResponse({'code': 200, 'msg': '请求成功'})
        else:
            return JsonResponse({'code': 203, 'msg': '请先设置封面图'})


'遇见人的列表'

@fn_timer
def user_friend(request):
    if request.method == 'POST':
        condition = request.POST['condition']
        lng = request.POST['lng']
        lat = request.POST['lat']
        gender = request.POST['gender']
        min_age = request.POST['min_age']
        max_age = request.POST['max_age']
        u = get_token(request)
        if not u:
            return JsonResponse({'code': 203, 'msg': '请先登录'})
        else:
            User.objects.filter(id=u.id).update(longitude=lng, latitude=lat)
            user_address = locatebyLatLng(lat, lng)
            user_add = geoadd(lng, lat, user_address)
            user_msgs = georadiusbymember(user_address, condition)
            count_list = len(user_msgs)
            if count_list <= 1:
                return JsonResponse({'code': 201, 'msg': '附近没人'})
            else:
                '请求一次就把遇见表清空'
                u.meetnum_set.all().delete()
                for user_msg in user_msgs:
                    user_site = user_msg[0]
                    user_distance = user_msg[1]
                    coordinate = geopos(user_site)
                    x = str(coordinate[0][0])[:10]
                    y = str(coordinate[0][1])[:9]
                    user_other = User.objects.filter(Q(latitude=y) & Q(longitude=x)).first()
                    if not user_other or u.id == user_other.id:
                        continue
                    else:
                        '遇见总人数'
                        '计算年龄'
                        dt = datetime.datetime.now()
                        age = dt.year - user_other.birth.year
                        # sex = '男' if user_other.gender == 0 else '女'
                        a = user_other.gender
                        if int(gender) == user_other.gender and age in range(int(min_age), int(max_age)):
                            meet_count = Count.objects.filter(user_id=u.id).first()
                            '遇见的人在不喜欢列表中出现两次，更换照片才能加入到遇见列表'
                            user_friend_photo = AddPhoto.objects.filter(user_id=user_other.id).first()
                            '查看是否在遇见表中'
                            meet_friend = u.meetnum_set.filter(meetcount=user_other.id)
                            '查看是否在喜欢表中'
                            meet_like_friend = u.meetlike_set.filter(friend_id=user_other.id)
                            '查看封面图在不喜欢列表中出现的次数'
                            meet_unlike_friend = u.meetunlike_set.filter(Q(friend_id=user_other.id) &
                                                                         Q(photo=user_friend_photo.image1.name)).all().count()
                            if meet_count and meet_unlike_friend < 2 and not meet_friend and not meet_like_friend:
                                count = meet_count.count
                                count += 1

                                u.meetnum_set.create(distance=user_distance, site=user_address,
                                                     age=age, meetcount=user_other.id, longitude=x,
                                                     latitude=y, gender=user_other.gender)
                                Count.objects.filter(user_id=u.id).update(count=count)
                            elif meet_unlike_friend >= 2 or meet_friend or meet_like_friend:
                                continue
                            else:
                                u.meetnum_set.create(distance=user_distance, site=user_address,
                                                     age=age, meetcount=user_other.id, longitude=x,
                                                     latitude=y, gender=user_other.gender)
                                Count.objects.create(user_id=u.id, count=1)
                        elif int(gender) == -1 and age in range(int(min_age), int(max_age)):
                            meet_count = Count.objects.filter(user_id=u.id).first()
                            '遇见的人在不喜欢列表中出现两次，更换照片才能加入到遇见列表'
                            user_friend_photo = AddPhoto.objects.filter(user_id=user_other.id).first()
                            meet_friend = u.meetnum_set.filter(meetcount=user_other.id)
                            meet_like_friend = u.meetlike_set.filter(friend_id=user_other.id)
                            meet_unlike_friend = u.meetunlike_set.filter(Q(friend_id=user_other.id) &
                                                                         Q(
                                                                             photo=user_friend_photo.image1.name)).all().count()
                            if meet_count and meet_unlike_friend < 2 and not meet_friend and not meet_like_friend:
                                count = meet_count.count
                                count += 1

                                u.meetnum_set.create(distance=user_distance, site=user_address,
                                                     age=age, meetcount=user_other.id, longitude=x,
                                                     latitude=y, gender=user_other.gender)
                                Count.objects.filter(user_id=u.id).update(count=count)
                            elif meet_unlike_friend >= 2 or meet_friend or meet_like_friend:
                                continue
                            else:
                                u.meetnum_set.create(distance=user_distance, site=user_address,
                                                     age=age, meetcount=user_other.id, longitude=x,
                                                     latitude=y, gender=user_other.gender)
                                Count.objects.create(user_id=u.id, count=1)
                        else:
                            continue
                return JsonResponse({'code': 200, 'msg': '请求成功'})


'用户添加照片'


def add_photo(request):
    if request.method == 'POST':
        user = get_token(request)
        img1 = request.POST.get('img1', None)
        img2 = request.POST.get('img2', None)
        img3 = request.POST.get('img3', None)
        img4 = request.POST.get('img4', None)
        img5 = request.POST.get('img5', None)
        img6 = request.POST.get('img6', None)
        if img1:
            try:
                img1 = base_image(img1)
                AddPhoto.objects.create(user_id=user.id, image1=img1)
            except Exception as e:
                return JsonResponse({'code': 201, 'msg': '上传失败'})
        if img2:
            try:
                img2 = base_image(img2)
                AddPhoto.objects.filter(user_id=user.id).update(image2=img2)
            except Exception as e:
                return JsonResponse({'code': 201, 'msg': '上传失败'})
        if img3:
            try:
                img3 = base_image(img3)
                AddPhoto.objects.filter(user_id=user.id).update(image3=img3)
            except Exception as e:
                return JsonResponse({'code': 201, 'msg': '上传失败'})
        if img4:
            try:
                img4 = base_image(img4)
                AddPhoto.objects.filter(user_id=user.id).update(image4=img4)
            except Exception as e:
                return JsonResponse({'code': 201, 'msg': '上传失败'})
        if img5:
            try:
                img5 = base_image(img5)
                AddPhoto.objects.filter(user_id=user.id).update(image5=img5)
            except Exception as e:
                return JsonResponse({'code': 201, 'msg': '上传失败'})
        if img6:
            try:
                img6 = base_image(img6)
                AddPhoto.objects.create(user_id=user.id, image6=img6)
            except Exception as e:
                return JsonResponse({'code': 201, 'msg': '上传失败'})
        return JsonResponse({'code': 200, 'msg': '请求成功'})


'用户删除照片'


def del_photo(request):
    if request.method == 'POST':
        user = get_token(request)
        img1 = request.POST.get('img1', None)
        img2 = request.POST.get('img2', None)
        img3 = request.POST.get('img3', None)
        img4 = request.POST.get('img4', None)
        img5 = request.POST.get('img5', None)
        img6 = request.POST.get('img6', None)
        if img1:
            AddPhoto.objects.filter(image1=img1).delete()
        if img2:
            AddPhoto.objects.filter(user_id=user.id).update(image2="")
        if img3:
            AddPhoto.objects.filter(user_id=user.id).update(image3="")
        if img4:
            AddPhoto.objects.filter(user_id=user.id).update(image4="")
        if img5:
            AddPhoto.objects.filter(user_id=user.id).update(image5="")
        if img6:
            AddPhoto.objects.filter(user_id=user.id).update(image6="")
        return JsonResponse({'code': 200, 'msg': '请求成功'})


'换封面图'


def exchange_img(request):
    if request.method == 'POST':
        user = get_token(request)
        img2 = request.POST.get('img2', None)
        img3 = request.POST.get('img3', None)
        img4 = request.POST.get('img4', None)
        img5 = request.POST.get('img5', None)
        img6 = request.POST.get('img6', None)
        img = user.addphoto_set.filter(user_id=user.id).first()
        img1 = img.image1.name
        if img2:
            AddPhoto.objects.filter(user_id=user.id).update(image1=img.image2.name)
            AddPhoto.objects.filter(user_id=user.id).update(image2=img1)
        if img3:
            AddPhoto.objects.filter(user_id=user.id).update(image1=img.image3.name)
            AddPhoto.objects.filter(user_id=user.id).update(image3=img1)
        if img4:
            AddPhoto.objects.filter(user_id=user.id).update(image1=img.image4.name)
            AddPhoto.objects.filter(user_id=user.id).update(image4=img1)
        if img5:
            AddPhoto.objects.filter(user_id=user.id).update(image1=img.image5.name)
            AddPhoto.objects.filter(user_id=user.id).update(image5=img1)
        if img6:
            AddPhoto.objects.filter(user_id=user.id).update(image1=img6.image6.name)
            AddPhoto.objects.filter(user_id=user.id).update(image6=img1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


'返回封面图'


def rack_img(request):
    if request.method == 'POST':
        user = get_token(request)
        user_image = AddPhoto.objects.filter(user_id=user.id).first()
        if user_image:
            data = dict(user_id=user.id, image1=user_image.image1.name, image2=user_image.image2.name,
                        image3=user_image.image3.name,
                        image4=user_image.image4.name, image5=user_image.image5.name, image6=user_image.image6.name)
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})

        else:
            return JsonResponse({'code': 201, 'msg': '先去添加照片'})


'遇见次数'


def meet_count(request):
    if request.method == 'GET':
        user_friend_id = request.GET['user_id']
        # user_id = request.session['user_id']
        user = User.objects.filter(id=1).first()
        if not user:
            return JsonResponse({'code': 203, 'msg': '请先登录'})
        else:
            meet_count = user.meetnum_set.filter(meetcount=user_friend_id).all().count()
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': meet_count})


'右滑左滑'


def slide(request):
    '我喜欢的人'
    if request.method == 'POST':
        liketype = request.POST['liketype']
        user_id = request.POST.get('friend_id')
        user = get_token(request)
        user_friend = User.objects.filter(id=user_id).first()
        user_friend_photo = AddPhoto.objects.filter(user_id=user_friend.id).first()
        meet_count = user.meetsite_set.filter(friend_id=user_id).first()
        friend_id = int(user_id)
        if liketype == '1':
            '右滑喜欢'
            count = user.meetlike_set.all().count()
            if meet_count:
                meet_count.nums += 1
                if count <= 52:
                    user.meetlike_set.create(friend_id=friend_id)
                    user.meetsite_set.filter(friend_id=friend_id).update(nums=meet_count.nums)
                    user.meetnum_set.filter(meetcount=user_id).delete()
                else:
                    return JsonResponse({'code': 202, 'msg': '喜欢人已满'})
            else:
                user.meetlike_set.create(friend_id=friend_id)
                MeetSite.objects.create(user_id=user.id, nums=1, friend_id=friend_id)
                user.meetnum_set.filter(meetcount=user_id).delete()
                return JsonResponse({'code': 200, 'msg': '请求成功'})
        if liketype == '0':
            '左滑不喜欢'
            if meet_count:
                meet_count.nums += 1
                user.meetunlike_set.create(photo=user_friend_photo.image1.name, friend_id=user_id
                                           )
                MeetSite.objects.filter(user_id=user.id).update(nums=meet_count.nums)
            else:
                user.meetunlike_set.create(photo=user_friend_photo.image1.name, friend_id=user_id)
                MeetSite.objects.create(user_id=user.id, nums=1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


'返回上一个不喜欢的用户'


def last_user(requset):
    if requset.method == 'GET':
        user = get_token(requset)
        lastuser = user.meetunlike_set.order_by('-id')
        if lastuser:
            x = lastuser[0]
            unuser = User.objects.filter(username=x.username).values()
            data = unuser[0]
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
        else:
            return JsonResponse({'code': 203, 'msg': '先去遇见人吧'})


'相遇点'


def meets_site(request):
    if request.method == 'POST':
        user_friend_id = request.POST.get('user_id')
        user = get_token(request)
        user_friend = User.objects.filter(id=user_friend_id).first()
        if not user:
            return JsonResponse({'code': 203, 'msg': '请先登录'})
        else:
            meet_user_id = user.meetnum_set.filter(meetcount=user_friend_id).all()
            result = []
            data = {}
            for meet_friend in meet_user_id:
                user_dict = {}
                user_friend_dict = {}
                lng = meet_friend.longitude
                lat = meet_friend.latitude
                meet_sites = meet_friend.site
                meet_coord = geopos(meet_sites)
                user_lng = str(meet_coord[0][0])[:10]
                user_lat = str(meet_coord[0][1])[:9]
                user_dict['user_lng'] = user_lng
                user_dict['user_lat'] = user_lat
                # user_dict['user_photo'] = user.photo
                user_friend_dict['lng'] = lng
                user_friend_dict['lat'] = lat
                # user_friend_dict['user_friend_photo'] = user_friend.photo
                # data['user'] = user_dict
                # data['user_friend'] = user_friend_dict
                result.append(user_dict)
                result.append(user_friend_dict)
            data['result'] = result
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})


'我喜欢的人、喜欢我的、相互喜欢的'


@cache_page(60 * 60)
def like_list(request):
    user = get_token(request)
    '我喜欢的人'
    user_likes = user.meetlike_set.all()
    data = {}
    result = []
    if user_likes.count() == 0:
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
    else:
        for user_like in user_likes:
            datas = {}
            '获取朋友对象'
            user_friends = User.objects.filter(pk=user_like.friend_id).first()
            '获取朋友的头像'
            user_img = user_friends.userimg_set.filter(img_type=1).first()
            user_img = user_img.img.name
            datas['user_id'] = user_friends.id
            datas['img'] = user_img
            datas['username'] = user_friends.username
            datas['like_time'] = user_like.like_time.strftime('%Y-%m-%d %H:%M:%S')
            result.append(datas)
        data['count'] = user_likes.count()
        data['result'] = result
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})


@cache_page(60 * 60)
def like_me(request):
    '喜欢我的人'
    u = get_token(request)
    user_meets = MeetLike.objects.filter(friend_id=u.id).all()
    data = {}
    result = []
    if user_meets:
        for user_meet in user_meets:
            be_likes = user_meet.user.all()
            count = user_meets.count()
            data['count'] = count
            for be_like in be_likes:
                d = {}
                belike = be_like.meetlike_set.filter(friend_id=u.id).first()
                user_img = be_like.userimg_set.filter(img_type=1).first()
                user_img = user_img.img.name
                d['user_id'] = be_like.id
                d['img'] = user_img
                d['username'] = be_like.username
                d['like_time'] = belike.like_time.strftime('%Y-%m-%d %H:%M:%S')
                result.append(d)
        data['result'] = result
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
    else:
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})


@cache_page(60 * 60)
def together_like(request):
    '相互喜欢'
    u = get_token(request)
    user_likes = u.meetlike_set.all()
    like_users = MeetLike.objects.filter(friend_id=u.id).all()
    data = {}
    result = []
    if user_likes and like_users:
        friend_list = []
        for user_like in user_likes:
            x = user_like.friend_id
            friend_list.append(x)
        for like_user in like_users:
            i = like_user.user.first()
            nums = 0
            if i.id in friend_list:
                d = {}
                nums += 1
                user_img = i.userimg_set.filter(img_type=1).first()
                user_img = user_img.img.name
                d['img'] = user_img
                d['username'] = i.username
                # d['like_time'] = i.like_time.strftime('%Y-%m-%d %H:%M:%S')
                d['count'] = nums
                result.append(d)
            else:
                return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
        data['result'] = result
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
    else:
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
