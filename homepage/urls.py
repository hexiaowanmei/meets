from django.urls import path
from homepage import views


urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('meet_count/', views.meet_count, name='meet_count'),
    path('slide/', views.slide, name='slide'),
    path('last_user/', views.last_user, name='last_user'),
    path('meets_site/', views.meets_site, name='meets_site'),
    path('user_friend/', views.user_friend, name='user_friend'),
    path('add_photo/', views.add_photo, name='add_photo'),
    path('del_photo/', views.del_photo, name='del_photo'),
    path('exchange_img/', views.exchange_img, name='exchange_img'),
    path('rack_img/', views.rack_img, name='rack_img'),
    path('like_list/', views.like_list, name='like_list'),
    path('like_me/', views.like_me, name='like_me'),
    path('together_like/', views.together_like, name='together_like'),
]