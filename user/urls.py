from django.urls import path
from user import views
# from user.views import ForCodeView

urlpatterns = [
    path('register/', views.register, name='register'),  # 注册
    path('detail_user/', views.detail_user, name='detail_user'),  # 完善信息
    path('add_label/', views.add_label, name='add_label'),  # 兴趣标签
    path('send_message/', views.send_message, name='send_message'),  # 发送短信
    path('login/', views.login, name='login'),  # 登录
    path('reset_pwd/', views.reset_pwd, name='reset_pwd'),  # 重置密码
    path('index/', views.index, name='index'),  # 我的
    path('update_index/', views.update_index, name='update_index'),  # 修改个人信息
    path('logout/', views.logout, name='logout'),  # 退出登录
    path('feedback/', views.feedback, name='feedback'),  # 用户反馈
]
