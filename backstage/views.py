from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from utils.function import get_token

# Create your views here.
from django.urls import reverse

from backstage.forms import Register, Login
from backstage.models import *
from utils.status_code import JsonRep


def index(request):
    if request.method == 'GET':
        return render(request, 'back/index.html')


def welcome(request):
    if request.method == 'GET':
        return render(request, 'back/welcome.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'back/login-page.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = BackUser.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'code': 201, 'msg': '不存在该用户'})
        if password is None or len(password) == 0:
            return JsonResponse({'code': 202, 'msg': '密码不能为空'})
        else:
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('backstage:index'))


def register(request):
    if request.method == 'GET':
        return render(request, 'back/register.html')
    if request.method == 'POST':
        username = request.POST.get('username', None)  # 手机号
        password = request.POST.get('password', None)  # 密码
        password1 = request.POST.get('password1', None)  # 密码

        user = BackUser.objects.filter(username=username).first()
        if user:
            return JsonResponse(JsonRep().FAILED(code=-5, msg='用户已注册请去登录'))
        if password != password1:
            return JsonResponse({'code': 201, 'msg': '两次密码不同'})
        try:
            BackUser.objects.create(username=username, password=make_password(password))

        except Exception as e:
            raise e
        return HttpResponseRedirect(reverse('backstage:login'))


'举报内容'


def report(request):
    pass
    # if request.method == 'GET':
    #     content = request.POST.get['content']
    #     content_text = request.POST.get['content_text']
    #     user = get_token(request)
    #     user_content = DynamicTalk.objects.filter(content_text=content_text).first()
    #     user = User.objects.filter(pk=user_content.id).first()
    #     ReportFriends.objects.create(cause=content)
    #     data = list[content, user_content.create_time, user_content.content_text]
    #     data = [1,2,3,4,5]
    #     c = '世间万物皆系于一箭之上'
    #     nums = len(data)
    #     return render(request, 'back/picture-list.html', {'c': c,
    #                                                       'data': data,
    #                                                       'nums': nums})



