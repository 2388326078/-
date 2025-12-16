from django.urls import path
from . import views

urlpatterns = [
    # 注册页面
    path('register/', views.user_register, name='user_register'),
    # 登录页面
    path('login/', views.user_login, name='user_login'),
    # 退出登录
    path('logout/', views.user_logout, name='user_logout'),
    # 个人中心（需要登录）
    path('profile/', views.user_profile, name='user_profile'),
]