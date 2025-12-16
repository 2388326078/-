from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import FileResponse
from django.db.models import Avg, Max, Min, Sum, Count
from django.utils import timezone
import os
import pandas as pd
from students.models import Student
from courses.models import Course
from scores.models import Score
from django.conf import settings

# 辅助函数：生成Excel文件路径
def get_excel_file_path(file_name):
    """返回Excel文件的完整路径"""
    return os.path.join(settings.EXPORT_ROOT, file_name)

def class_analysis(request):
    """班级成绩分析：按班级分组，计算每个班级的平均分、最高分、最低分、参与人数等"""
    # 1. 按班级分组，关联学生和成绩表，聚合统计
    # 思路：先筛选有成绩的学生，按班级分组，计算成绩的各项指标
    class_analysis_list = Student.objects.filter(
        scores__isnull=False  # 只选有成绩的学生
    ).values(
        'class_name'  # 分组字段：班级名称
    ).annotate(
        # 聚合计算：班级平均分（scores__score是学生的成绩字段）
        avg_score=Avg('scores__score'),
        # 班级最高分
        max_score=Max('scores__score'),
        # 班级最低分
        min_score=Min('scores__score'),
        # 班级参与人数（去重，因为一个学生可能有多门课成绩）
        student_count=Count('student_id', distinct=True),
        # 班级成绩总条数
        score_count=Count('scores__score')
    ).order_by('class_name')  # 按班级名称排序

    # 2. 处理数据（保留两位小数，提升可读性）
    for item in class_analysis_list:
        item['avg_score'] = round(item['avg_score'], 2) if item['avg_score'] else 0.0
        item['max_score'] = round(item['max_score'], 2) if item['max_score'] else 0.0
        item['min_score'] = round(item['min_score'], 2) if item['min_score'] else 0.0

    context = {
        'analysis_list': class_analysis_list,
        'title': '班级成绩分析'
    }
    return render(request, 'analysis/analysis_result.html', context)

def course_analysis(request):
    """课程成绩分析：按课程分组，计算每门课程的平均分、最高分、最低分、参与人数等"""
    # 1. 按课程分组，关联课程和成绩表，聚合统计
    course_analysis_list = Course.objects.filter(
        scores__isnull=False  # 只选有成绩的课程
    ).values(
        'course_id', 'course_name'  # 分组字段：课程编号、课程名称
    ).annotate(
        avg_score=Avg('scores__score'),
        max_score=Max('scores__score'),
        min_score=Min('scores__score'),
        # 参与人数（去重，一个学生可能选一门课）
        student_count=Count('scores__student', distinct=True),
        # 成绩总条数
        score_count=Count('scores__score')
    ).order_by('course_id')  # 按课程编号排序

    # 2. 处理数据
    for item in course_analysis_list:
        item['avg_score'] = round(item['avg_score'], 2) if item['avg_score'] else 0.0
        item['max_score'] = round(item['max_score'], 2) if item['max_score'] else 0.0
        item['min_score'] = round(item['min_score'], 2) if item['min_score'] else 0.0

    context = {
        'analysis_list': course_analysis_list,
        'title': '课程成绩分析'
    }
    return render(request, 'analysis/analysis_result.html', context)

def student_ranking(request):
    """学生排名：按总分/平均分排序，标注名次"""
    # 1. 按学生分组，计算每个学生的总分、平均分、课程数
    student_score_list = Student.objects.filter(
        scores__isnull=False
    ).values(
        'student_id', 'name', 'class_name'  # 学生学号、姓名、班级
    ).annotate(
        total_score=Sum('scores__score'),  # 总分
        avg_score=Avg('scores__score'),    # 平均分
        course_count=Count('scores__course')  # 修课数
    ).order_by('-total_score', '-avg_score')  # 先按总分降序，再按平均分降序

    # 2. 标注名次（注意：同分的情况，这里简单处理为连续名次，也可以实现并列名次）
    student_ranking_list = []
    rank = 1
    for item in student_score_list:
        item['rank'] = rank
        item['total_score'] = round(item['total_score'], 2) if item['total_score'] else 0.0
        item['avg_score'] = round(item['avg_score'], 2) if item['avg_score'] else 0.0
        student_ranking_list.append(item)
        rank += 1

    context = {
        'analysis_list': student_ranking_list,
        'title': '学生成绩排名'
    }
    return render(request, 'analysis/analysis_result.html', context)

def export_excel(request, analysis_type):
    """导出Excel文件：根据分析类型（class/course/student）导出对应数据"""
    # 1. 根据分析类型获取数据（复用之前的查询逻辑）
    if analysis_type == 'class':
        # 班级分析数据
        data = list(Student.objects.filter(scores__isnull=False).values(
            'class_name'
        ).annotate(
            avg_score=Avg('scores__score'),
            max_score=Max('scores__score'),
            min_score=Min('scores__score'),
            student_count=Count('student_id', distinct=True),
            score_count=Count('scores__score')
        ).order_by('class_name'))
        # 处理数据格式
        for item in data:
            item['avg_score'] = round(item['avg_score'], 2) if item['avg_score'] else 0.0
            item['max_score'] = round(item['max_score'], 2) if item['max_score'] else 0.0
            item['min_score'] = round(item['min_score'], 2) if item['min_score'] else 0.0
        file_name = f"班级成绩分析_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        sheet_name = "班级分析"
    elif analysis_type == 'course':
        # 课程分析数据
        data = list(Course.objects.filter(scores__isnull=False).values(
            'course_id', 'course_name'
        ).annotate(
            avg_score=Avg('scores__score'),
            max_score=Max('scores__score'),
            min_score=Min('scores__score'),
            student_count=Count('scores__student', distinct=True),
            score_count=Count('scores__score')
        ).order_by('course_id'))
        for item in data:
            item['avg_score'] = round(item['avg_score'], 2) if item['avg_score'] else 0.0
            item['max_score'] = round(item['max_score'], 2) if item['max_score'] else 0.0
            item['min_score'] = round(item['min_score'], 2) if item['min_score'] else 0.0
        file_name = f"课程成绩分析_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        sheet_name = "课程分析"
    elif analysis_type == 'student':
        # 学生排名数据
        data = list(Student.objects.filter(scores__isnull=False).values(
            'student_id', 'name', 'class_name'
        ).annotate(
            total_score=Sum('scores__score'),
            avg_score=Avg('scores__score'),
            course_count=Count('scores__course')
        ).order_by('-total_score', '-avg_score'))
        # 标注名次
        rank = 1
        for item in data:
            item['rank'] = rank
            item['total_score'] = round(item['total_score'], 2) if item['total_score'] else 0.0
            item['avg_score'] = round(item['avg_score'], 2) if item['avg_score'] else 0.0
            rank += 1
        file_name = f"学生成绩排名_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        sheet_name = "学生排名"
    else:
        # 无效的分析类型
        return render(request, 'analysis/error.html', {'msg': '无效的分析类型！'})

    # 2. 将数据转为pandas的DataFrame
    df = pd.DataFrame(data)

    # 3. 保存为Excel文件（使用openpyxl引擎）
    file_path = get_excel_file_path(file_name)
    df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')

    # 4. 返回文件给前端下载（使用FileResponse，自动处理文件下载）
    # 注意：mode='rb'表示以二进制只读模式打开
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    return response