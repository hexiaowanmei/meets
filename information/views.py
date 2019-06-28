from django.shortcuts import render

from user.models import UserImg, User
from utils.function import get_token
from information.models import Chat
from django.http import JsonResponse


# Create your views here.

def chat_info(request):
    '存储聊天信息'
    user = get_token(request)
    friend_id = request.POST.get('friend_id')
    content = request.POST.get('content')
    try:
        user.chat_set.create(friend_id=friend_id, content=content)
    except Exception as e:
        return JsonResponse({'code': 201, 'msg': '请求失败'})
    return JsonResponse({'code': 200, 'msg': '请求成功'})


def msg_info(requset):
    '返回聊天信息'
    user = get_token(requset)
    friend_id = requset.POST.get('friend_id')
    user_contents = user.chat_set.filter(friend_id=friend_id).order_by('-id')
    user_img = UserImg.objects.filter(user_id=user.id).first()
    data = {}
    user_result = []
    friend_result = []
    '获取自己的聊天信息'
    if user_contents:
        for user_content in user_contents:
            d = {}
            d['user_content'] = user_content.content
            d['time'] = user_content.chat_time.strftime('%Y-%m-%d %H:%M:%S')
            user_result.append(d)
        user_result.append(user_img.img.name)
    else:
        user_result = []
    '获取朋友的聊天信息'
    friend = User.objects.filter(pk=friend_id).frist()
    friend_img = UserImg.objects.filter(user_id=friend_id).first()
    friend_contents = friend.chat_set.filter(user_id=user.id).order_by('id')
    if friend_contents:
        for friend_content in friend_contents:
            d = {}
            d['user_content'] = friend_content.content
            d['time'] = friend_content.chat_time.strftime('%Y-%m-%d %H:%M:%S')
            friend_result.append(d)
        friend_result.append(friend_img.img.name)
    else:
        friend_result = []
    data['user_result'] = user_result
    data['friend_result'] = friend_result
    return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
