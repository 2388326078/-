from django.shortcuts import render, redirect, get_object_or_404
from scores.models import Score
from students.models import Student
from courses.models import Course

def score_list(request):
    """成绩列表+查询"""
    # 获取查询条件（可以按学生学号、姓名、课程名称查询）
    student_id = request.GET.get("student_id", "")
    student_name = request.GET.get("student_name", "")
    course_name = request.GET.get("course_name", "")

    # 拼接查询条件（使用连表查询）
    score_queryset = Score.objects.all().order_by("-update_time")
    if student_id:
        # 关联学生表，按学号查询
        score_queryset = score_queryset.filter(student__student_id__contains=student_id)
    if student_name:
        # 关联学生表，按姓名查询
        score_queryset = score_queryset.filter(student__name__contains=student_name)
    if course_name:
        # 关联课程表，按课程名称查询
        score_queryset = score_queryset.filter(course__course_name__contains=course_name)

    context = {
        "score_list": score_queryset,
        "student_id": student_id,
        "student_name": student_name,
        "course_name": course_name,
    }
    return render(request, "scores/score_list.html", context)

def score_add(request):
    """新增成绩（核心：校验学生+课程的唯一性）"""
    if request.method == "POST":
        # 获取前端提交的参数
        student_id = request.POST.get("student")  # 学生学号
        course_id = request.POST.get("course")    # 课程编号
        score = request.POST.get("score")
        exam_time = request.POST.get("exam_time", None)

        # 数据验证
        error_msg = ""
        # 1. 校验基础字段
        if not student_id or not course_id or not score:
            error_msg = "学生、课程、成绩不能为空！"
        # 2. 校验成绩范围（0-100）
        try:
            score = float(score)
            if score < 0 or score > 100:
                error_msg = "成绩必须在0-100之间！"
        except ValueError:
            error_msg = "成绩必须是数字！"
        # 3. 校验学生和课程是否存在
        student = None
        course = None
        if not error_msg:
            try:
                student = Student.objects.get(student_id=student_id)
                course = Course.objects.get(course_id=course_id)
            except (Student.DoesNotExist, Course.DoesNotExist):
                error_msg = "学生或课程不存在！"
        # 4. 校验学生+课程的组合是否已存在（业务层面校验，数据库也有约束）
        if not error_msg and Score.objects.filter(student=student, course=course).exists():
            error_msg = f"该学生的{course.course_name}课程成绩已存在！"

        if error_msg:
            # 若验证失败，需要把所有学生和课程回显到下拉框
            students = Student.objects.all().order_by("student_id")
            courses = Course.objects.all().order_by("course_id")
            return render(request, "scores/score_add.html", {
                "error_msg": error_msg,
                "students": students,
                "courses": courses,
                "selected_student": student_id,  # 回显选中的学生
                "selected_course": course_id     # 回显选中的课程
            })

        # 保存数据
        score_obj = Score(
            student=student,
            course=course,
            score=score,
            exam_time=exam_time
        )
        score_obj.save()

        return redirect("score_list")

    # GET请求：获取所有学生和课程，供前端下拉框选择
    students = Student.objects.all().order_by("student_id")
    courses = Course.objects.all().order_by("course_id")
    return render(request, "scores/score_add.html", {
        "students": students,
        "courses": courses
    })

def score_edit(request, score_id):
    """修改成绩（核心：只更新成绩和考试时间，学生和课程不可改）"""
    score_obj = get_object_or_404(Score, id=score_id)

    if request.method == "POST":
        # 注意：这里不接收student和course参数，只接收成绩和考试时间
        new_score = request.POST.get("score")
        exam_time = request.POST.get("exam_time", None)

        # 数据验证
        error_msg = ""
        if not new_score:
            error_msg = "成绩不能为空！"
        try:
            new_score = float(new_score)
            if new_score < 0 or new_score > 100:
                error_msg = "成绩必须在0-100之间！"
        except ValueError:
            error_msg = "成绩必须是数字！"

        if error_msg:
            return render(request, "scores/score_edit.html", {
                "error_msg": error_msg,
                "score": score_obj
            })

        # 只更新成绩和考试时间，学生和课程保持不变
        score_obj.score = new_score
        if exam_time:
            score_obj.exam_time = exam_time
        score_obj.save()

        return redirect("score_list")

    # GET请求：返回修改页面，传递成绩信息（学生和课程不可改，只做展示）
    return render(request, "scores/score_edit.html", {"score": score_obj})

def score_delete(request, score_id):
    """删除成绩"""
    score_obj = get_object_or_404(Score, id=score_id)
    score_obj.delete()
    return redirect("score_list")