from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course

def course_list(request):
    """课程列表+查询"""
    # 获取查询条件
    course_id = request.GET.get("course_id", "")
    course_name = request.GET.get("course_name", "")

    # 拼接查询条件
    course_queryset = Course.objects.all().order_by("-update_time")
    if course_id:
        course_queryset = course_queryset.filter(course_id__contains=course_id)
    if course_name:
        course_queryset = course_queryset.filter(course_name__contains=course_name)

    context = {
        "course_list": course_queryset,
        "course_id": course_id,
        "course_name": course_name,
    }
    return render(request, "courses/course_list.html", context)

def course_add(request):
    """新增课程"""
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
        description = request.POST.get("description", "")

        # 数据验证
        error_msg = ""
        if not course_id:
            error_msg = "课程编号不能为空！"
        elif not course_name:
            error_msg = "课程名称不能为空！"
        elif Course.objects.filter(course_id=course_id).exists():
            error_msg = "该课程编号已存在！"
        elif Course.objects.filter(course_name=course_name).exists():
            error_msg = "该课程名称已存在！"

        if error_msg:
            return render(request, "courses/course_add.html", {"error_msg": error_msg})

        # 保存数据
        course = Course(
            course_id=course_id,
            course_name=course_name,
            description=description
        )
        course.save()

        return redirect("course_list")

    return render(request, "courses/course_add.html")

def course_edit(request, course_id):
    """修改课程"""
    course = get_object_or_404(Course, course_id=course_id)

    if request.method == "POST":
        course_name = request.POST.get("course_name")
        description = request.POST.get("description", "")

        # 数据验证
        error_msg = ""
        if not course_name:
            error_msg = "课程名称不能为空！"
        elif Course.objects.filter(course_name=course_name).exclude(course_id=course_id).exists():
            # 排除当前课程，检查其他课程是否有同名
            error_msg = "该课程名称已存在！"

        if error_msg:
            return render(request, "courses/course_edit.html", {"error_msg": error_msg, "course": course})

        # 更新数据（课程编号不允许修改）
        course.course_name = course_name
        course.description = description
        course.save()

        return redirect("course_list")

    return render(request, "courses/course_edit.html", {"course": course})

def course_delete(request, course_id):
    """删除课程"""
    course = get_object_or_404(Course, course_id=course_id)
    course.delete()
    return redirect("course_list")