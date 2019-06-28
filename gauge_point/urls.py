from django.urls import path
from gauge_point import views

urlpatterns = [
    path('issue_gauge/', views.issue_gauge, name='issue_gauge'),  # 发布标记点
    path('like_gauge/', views.like_gauge, name='like_gauge'),  # 点赞
    path('report_gauge/', views.report_gauge, name='report_gauge'),  # 举报标记点
    path('del_gauge/', views.del_gauge, name='del_gauge'),  # 删除标记点
    # path('content_audit/', views.content_audit, name='content_audit'),  # 内容审核

]