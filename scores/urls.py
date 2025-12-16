from django.urls import path
from . import views

urlpatterns = [
    # 成绩列表/查询
    path('list/', views.score_list, name='score_list'),
    # 新增成绩
    path('add/', views.score_add, name='score_add'),
    # 修改成绩
    path('edit/<int:score_id>/', views.score_edit, name='score_edit'),
    # 删除成绩
    path('delete/<int:score_id>/', views.score_delete, name='score_delete'),
]