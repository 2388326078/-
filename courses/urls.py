from django.urls import path
from . import views

urlpatterns = [
    # 课程列表/查询
    path('list/', views.course_list, name='course_list'),
    # 新增课程
    path('add/', views.course_add, name='course_add'),
    # 修改课程
    path('edit/<str:course_id>/', views.course_edit, name='course_edit'),
    # 删除课程
    path('delete/<str:course_id>/', views.course_delete, name='course_delete'),
]