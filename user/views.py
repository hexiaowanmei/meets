import re
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse

from rest_framework.decorators import api_view

from dynamictalk.models import DynamicTalk
from gauge_point.models import Gauge_Point
from homepage.models import AddPhoto, MeetLike
from user.models import UserImg, Lable, Feedback
from utils.function import *
from utils.redis_test import OPRedis
from utils.status_code import JsonRep
from utils.tenxunyun import TengXun, Random_verify

opr = OPRedis()
MOBILE_RE = '^1[3456789]\d{9}$'


# 发送短信验证码
@api_view(['POST', 'GET'])
def send_message(request):
    # 第一步 request.GET --> dict(key , value)  ['Name'] / get('Name')
    mobile = request.POST.get('mobile', None)
    # /user/send_message?mobile=
    if mobile is None or len(mobile) == 0:
        return JsonResponse(JsonRep().FAILED(code=-1, msg='没有传递参数mobile'))
    if not re.match(MOBILE_RE, mobile):
        return JsonResponse(JsonRep().FAILED(code=-2, msg='请输入正确手机号'))
    tengxun = TengXun()
    code = Random_verify()
    results = tengxun.send_message(code, mobile)
    try:
        if results['result'] == 0:
            # request.session.setdefault(mobile, code) 存在就不能设置
            # request.session[mobile] = code
            opr.setredis(mobile, code)
        else:
            return JsonResponse(JsonRep().FAILED(code=-3, msg='发送失败'))
    except Exception as e:
        print(e)
        return JsonResponse(JsonRep().FAILED(code=-3, msg='发送失败'))
    return JsonResponse(JsonRep().SUCCESS(msg='发送成功！有效期10分钟'))

@api_view(['POST', 'GET'])
# 注册用户
def register(request):
    mobile = request.POST.get('mobile', None)  # 手机号
    password = request.POST.get('password', None)  # 密码
    verify = request.POST.get('verify', None)  # 验证码
    if mobile is None or len(mobile) == 0:
        return JsonResponse(JsonRep().FAILED(code=-1, msg='没有传递参数mobile'))
    if password is None or len(password) == 0:
        return JsonResponse(JsonRep().FAILED(code=-2, msg='密码不能为空'))
    if not re.match(MOBILE_RE, mobile):
        return JsonResponse(JsonRep().FAILED(code=-3, msg='请输入正确手机号'))
    user = User.objects.filter(mobile=mobile).first()
    if user:
        return JsonResponse(JsonRep().FAILED(code=-5, msg='用户已注册请去登录'))
    code = opr.getredis(mobile)
    # 如果code is None 就是False  / code is not None 就是True
    if code != verify:
        return JsonResponse(JsonRep().FAILED(code=-4, msg='验证错误，请重新发送验证码'))
    user_code = random_id()
    try:
        user = User.objects.create(mobile=mobile, password=make_password(password), code_id=user_code)
        # request.session['user_id'] = user.id
        data = dict(id=user.id, mobile=mobile, password=password, code_id=user_code, verify=verify)
        # 创建成功后清除redis中该key值
        opr.delredis(mobile)
    except Exception as e:
        raise e
    return JsonResponse(JsonRep().SUCCESS(msg='注册成功！', data=data))


@api_view(['POST', 'GET'])
def detail_user(request):
    user_id = request.POST.get('user_id')
    head_portrait = request.POST.get('head_portrait', None)
    username = request.POST.get('username', None)
    gender = request.POST.get('gender', None)
    birth = request.POST.get('birth', None)
    scope = request.POST.get('scope', None)
    signature = request.POST.get('signature', None)
    latitude = request.POST.get('latitude', 0)
    longitude = request.POST.get('longitude', 0)
    # print(get_constellation(8, 23))

    img = base_image(head_portrait)
    # imgdata = base64.b64decode(head_portrait)
    # file = open('./media/upload/aa.jpg', 'wb')
    # file.write(imgdata)
    # file.close()
    # user = get_User(request)
    # user = User.objects.filter(pk=user_id).first()
    user = get_token(request)
    if user:
        try:
            user.username = username  # if not username else user.mobile
            user.gender = gender
            user.birth = birth
            user.scope = scope
            user.signature = signature
            user.latitude = latitude
            user.longitude = longitude
            user.save()
            UserImg(user_id=user.id, img=img, img_type=1).save()

        except Exception as e:
            return JsonResponse({'code': 201, 'msg': '完善信息失败'})
        img = user.userimg_set.filter(img_type=1).first()
        data = dict(id=user.id, username=user.username, gender=user.gender,
                    birthday=user.birth, scope=user.scope, signature=user.signature,
                    img=img.img.name, code_id=user.code_id)
        return JsonResponse(JsonRep().SUCCESS(msg='完善信息成功！', data=data))
    return JsonResponse(JsonRep().FAILED(msg='完善信息失败'))


# 用户信息完善
@api_view(['POST', 'GET'])
def add_label(request):
    lables = request.POST.get('lables', None)
    lables_list = [] if len(lables) == 0 or lables is None else lables.split(',')
    try:
        user = get_token(request)

        if user:
            [Lable(user=user, lable=labels).save() for labels in lables_list]
            return JsonResponse(JsonRep().SUCCESS(msg='设置标签成功'))
        else:
            return JsonResponse(JsonRep().FAILED(msg='设置标签失败'))
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(msg='设置标签失败'))


# 重置修改密码
@api_view(['POST', 'GET'])
def reset_pwd(request):
    mobile = request.POST.get('mobile', None)
    password = request.POST.get('password', None)
    verify = request.POST.get('verify', None)
    if not all([mobile, password, verify]):
        return JsonResponse(JsonRep().FAILED(msg='必要参数没有传递'))
    user = get_token(request)
    if verify != opr.getredis(mobile):
        return JsonResponse(JsonRep().FAILED(code=-2, msg='短信验证失败'))
    if not user:
        return JsonResponse(JsonRep().FAILED(code=-3, msg='用户验证失败'))
    user.password = make_password(password)
    user.save()
    return JsonResponse(JsonRep().SUCCESS(msg='重置密码成功'))
@api_view(['POST', 'GET'])
def send_message(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile', None)
        # /user/send_message?mobile=
        if mobile is None or len(mobile) == 0:
            return JsonResponse(JsonRep().FAILED(code=-1, msg='没有传递参数mobile'))
        if not re.match(MOBILE_RE, mobile):
            return JsonResponse(JsonRep().FAILED(code=-2, msg='请输入正确手机号'))
        tengxun = TengXun()
        code = Random_verify()
        results = tengxun.send_message(code, mobile)
        try:
            if results['result'] == 0:
                # request.session.setdefault(mobile, code) 存在就不能设置
                # request.session[mobile] = code
                opr.setredis(mobile, code)
            else:
                return JsonResponse(JsonRep().FAILED(code=-3, msg='发送失败'))
        except Exception as e:
            print(e)
            return JsonResponse(JsonRep().FAILED(code=-3, msg='发送失败'))
        return JsonResponse(JsonRep().SUCCESS(msg='发送成功！有效期10分钟'))


# # 登录
# @csrf_exempt
@api_view(['POST', 'GET'])
def login(request):
    mobile = request.POST.get('mobile', None)  # 手机号
    password = request.POST.get('password', None)  # 密码
    verify = request.POST.get('verify', None)  # 验证码
    if mobile is None or len(mobile) == 0:
        return JsonResponse(JsonRep().FAILED(code=-1, msg='没有传递参数mobile'))
    if not re.match(MOBILE_RE, mobile):
        return JsonResponse(JsonRep().FAILED(code=-3, msg='请输入正确手机号'))
    user = User.objects.filter(mobile=mobile).first()
    if not user:
        return JsonResponse(JsonRep().FAILED(code=-5, msg='不存在该用户'))
    if password is None or len(password) == 0:
        try:
            # 如果code is None 就是False  / code is not None 就是True
            code = opr.getredis(mobile)
            if code != verify:
                return JsonResponse(JsonRep().FAILED(code=-4, msg='验证错误，请重新发送验证码'))
            return JsonResponse(JsonRep().SUCCESS(msg='登录成功！'))
        except Exception as e:
            print(e)
            return JsonResponse({'code': -1, 'msg': '不存在该用户！'})
    else:
        if check_password(password, user.password):
            s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
            token = ''
            for i in range(20):
                token += random.choice(s)
            us_token = UserToken.objects.filter(user_id=user.id).first()
            if us_token:
                UserToken.objects.filter(user_id=user.id).update(token=token)
            else:
                UserToken.objects.create(user_id=user.id, token=token)
            if_complete = user.username
            if_complete_index_img = AddPhoto.objects.filter(user_id=user.id).first()
            if if_complete:
                user_img = UserImg.objects.filter(user_id=user.id).first()
                if if_complete_index_img:
                    data = dict(id=user.id, mobile=user.mobile, username=user.username, if_complete_index_img=True,
                                code_id=user.code_id, img=user_img.img.name, if_complete=True, token=token)
                    return JsonResponse(JsonRep().SUCCESS(msg='登录成功！', data=data))
                else:
                    data = dict(id=user.id, mobile=user.mobile, username=user.username, if_complete_index_img=False,
                                code_id=user.code_id, img=user_img.img.name, if_complete=True, token=token)
                    return JsonResponse(JsonRep().SUCCESS(msg='登录成功！', data=data))

            else:
                if if_complete_index_img:
                    data = dict(id=user.id, mobile=user.mobile, if_complete=False, if_complete_index_img=True,
                                token=token)
                    return JsonResponse(JsonRep().SUCCESS(msg='登录成功！', data=data))
                else:
                    data = dict(id=user.id, mobile=user.mobile, if_complete=False, if_complete_index_img=False,
                                token=token)
                    return JsonResponse(JsonRep().SUCCESS(msg='登录成功！', data=data))
    return JsonResponse(JsonRep().FAILED(code=-6, msg='校验失败'))

# 我的
@api_view(['GET', 'POST'])
def index(request):
    # 查看个人信息
    if request.method == 'POST':
        user = get_token(request)
        if not user:
            return JsonResponse(JsonRep().FAILED(code=-3, msg='用户不存在'))
        index_dict = {}
        dt = datetime.datetime.now()
        age = dt.year - user.birth.year
        # 获取我喜欢、喜欢我、相互喜欢数量
        user_likes = user.meetlike_set.all().count()
        like_users = MeetLike.objects.filter(friend_id=user.id).all().count()
        if user_likes and like_users:
            friend_list = []
            for user_like in user_likes:
                x = user_like.friend_id
                friend_list.append(x)
            for like_user in like_users:
                i = like_user.user.first()
                nums = 0
                if i.id in friend_list:
                    nums += 1
                index_dict['together_like_count'] = nums
        friend_count = DynamicTalk.objects.filter(user_id=user.id).all().count()
        # gauge_count = Gauge_Point.objects.filter(user_id=user.id).all().count()
        img = user.userimg_set.filter(img_type=1).first()
        index_dict['img'] = img.img.name
        index_dict['username'] = user.username
        index_dict['gender'] = user.gender
        index_dict['age'] = age
        index_dict['code_id'] = user.code_id
        index_dict['user_like_count'] = user_likes
        index_dict['user_meet_count'] = like_users
        index_dict['friend_count'] = friend_count
        # index_dict['gauge_coutn'] = gauge_count
        # index_dict['together_like_count'] = together_like_count
        return JsonResponse(JsonRep().SUCCESS(msg='请求成功', data=index_dict))


@api_view(['GET', 'POST'])
def update_index(request):
    # 修改用户信息
    if request.method == 'POST':
        # 相册
        imgs = request.POST.get('imgs', None)
        username = request.POST.get('username', None)
        code_id = request.POST.get('code_id', None)
        gender = request.POST.get('gender', None)
        birth = request.POST.get('birth', None)
        scope = request.POST.get('scope', None)
        signature = request.POST.get('signature', None)
        if not all([username, code_id]):
            return JsonResponse(JsonRep().FAILED(msg='必要参数没有传递'))
        user = get_token(request)
        try:
            if user:
                user.username = username
                user.gender = gender
                user.birth = birth
                user.scope = scope
                user.signature = signature
                if not user.is_alter:
                    user.code_id = code_id
                user.save()

            user.userimg_set.all().delete()
            img = base_image(imgs)
            UserImg(user=user, img=img, img_type=1).save()

            return JsonResponse(JsonRep().SUCCESS(msg='保存成功'))
        except Exception as e:
            print('==================\n', e, '==================\n')
            return JsonResponse(JsonRep().FAILED(code=-2, msg='保存失败'))


@api_view(['GET'])
def feedback(request):
    centent = request.GET.get('centent', None)
    user = get_token(request)
    try:
        Feedback(user=user, centent=centent).save()
        return JsonResponse(JsonRep().SUCCESS(msg='反馈成功'))
    except Exception as e:
        print('==================\n', e, '==================\n')
        return JsonResponse(JsonRep().FAILED(msg='反馈失败'))


# 用户退出
@api_view(['GET', 'POST'])
def logout(request):
    if request.method == 'POST':
        user = get_token(request)
        UserToken.objects.filter(user_id=user.id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})
