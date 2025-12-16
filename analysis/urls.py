from django.urls import path
from . import views

urlpatterns = [
    # 班级成绩分析
    path('class_analysis/', views.class_analysis, name='class_analysis'),
    # 课程成绩分析
    path('course_analysis/', views.course_analysis, name='course_analysis'),
    # 学生排名
    path('student_ranking/', views.student_ranking, name='student_ranking'),
    # 导出Excel（接收分析类型参数：class/course/student）
    path('export_excel/<str:analysis_type>/', views.export_excel, name='export_excel'),
]