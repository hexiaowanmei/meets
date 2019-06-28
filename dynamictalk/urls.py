from django.urls import path
from dynamictalk import views

urlpatterns = [
    path('issue_friend/', views.issue_friend, name='issue_friend'),  # 发布朋友圈
    path('check_friend/', views.check_friend, name='check_friend'),  # 查看朋友圈
    path('like_friend/', views.like_friend, name='like_friends'),  # 朋友圈点赞
    path('report_friend/', views.report_friend, name='report_friends'),  # 朋友圈举报
    path('del_friend/', views.del_friend, name='del_friend'),  # 朋友圈删除
    path('check_index/', views.check_index, name='check_index'),  # 内容审核
]