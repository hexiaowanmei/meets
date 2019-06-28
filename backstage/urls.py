from django.urls import path
from backstage import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('report/', views.report, name='report'),
    path('welcome/', views.welcome, name='welcome'),
]