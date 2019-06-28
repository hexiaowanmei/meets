import base64
import datetime

from django.http import JsonResponse

from user.models import User, UserToken
import random


# 从session中获取user
def get_User(request):
    try:
        pk = request.session.get('user_id')
        user = User.objects.get(pk=pk)
        return user
    except Exception as e:
        print('==================\n', e, '==================\n')
        return None


# 获取token值
def get_token(request):
    token = request.POST.get('token')
    user_token = UserToken.objects.filter(token=token).first()
    if user_token:
        user = User.objects.filter(id=user_token.user_id).first()
        return user
    else:
        JsonResponse({'code': 201, 'msg': '请先登录'})


# 获取最近7天
def get_end_by_dt_7(dt):
    dt_list = list()
    for i in range(7):
        oneday = datetime.timedelta(days=i)
        day = dt - oneday
        date_to = datetime.datetime(day.year, day.mouth, day.day)
        dt_list.append(date_to)
    return dt_list[-1]


# 生成随机ID
sr = '1234567890'


def random_id():
    nums = ''
    for i in range(7):
        nums += random.choice(sr)
    return nums


# 解密图片

s = '1234567890qwertyuiopasdfghQWERTYUIOPASDFGHJKLZXCVBNMjkl'


def base_image(image):
    img = ''
    for i in range(8):
        img += random.choice(s)

    data = base64.b64decode(image)
    # path = '/media/upload/%s.jpg' % img
    with open('./media/upload/%s.jpg' % img, 'wb') as f:
        f.write(data)
        f.close()

    return '/media/upload/' + img + '.jpg'


import time
from functools import wraps
import random


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s seconds" %
              (str(t1 - t0))
              )
        return result

    return function_timer