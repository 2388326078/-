from django.urls import path
from . import views

urlpatterns = [
    # 学生信息列表/查询
    path('list/', views.student_list, name='student_list'),
    # 新增学生
    path('add/', views.student_add, name='student_add'),
    # 修改学生（接收学号参数）
    path('edit/<str:student_id>/', views.student_edit, name='student_edit'),
    # 删除学生（接收学号参数）
    path('delete/<str:student_id>/', views.student_delete, name='student_delete'),
]