from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from users.views import login_required

@login_required
def student_list(request):
    """学生信息列表+综合查询"""
    # 1. 获取前端传递的查询条件（request.GET是获取URL中的参数，比如?student_id=1001&name=张三）
    student_id = request.GET.get("student_id", "")  # 学号，默认空字符串
    name = request.GET.get("name", "")  # 姓名，默认空字符串
    class_name = request.GET.get("class_name", "")  # 班级，默认空字符串

    # 2. 拼接查询条件（链式filter，只有当条件非空时才添加）
    # 先获取所有学生的查询集（QuerySet）
    student_queryset = Student.objects.all().order_by("-update_time")  # 按更新时间倒序
    # 如果学号非空，添加学号模糊查询（__contains是包含，__exact是精确匹配）
    if student_id:
        student_queryset = student_queryset.filter(student_id__contains=student_id)
    # 如果姓名非空，添加姓名模糊查询
    if name:
        student_queryset = student_queryset.filter(name__contains=name)
    # 如果班级非空，添加班级模糊查询
    if class_name:
        student_queryset = student_queryset.filter(class_name__contains=class_name)

    # 3. 将查询结果和查询条件传递给前端模板
    context = {
        "student_list": student_queryset,  # 查询结果
        "student_id": student_id,  # 回显查询条件
        "name": name,
        "class_name": class_name,
    }
    return render(request, "students/student_list.html", context)


def student_add(request):
    """新增学生"""
    if request.method == "POST":
        # 1. 获取前端提交的表单数据（request.POST是普通字段，request.FILES是文件字段）
        student_id = request.POST.get("student_id")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        class_name = request.POST.get("class_name")
        age = request.POST.get("age")
        phone = request.POST.get("phone", "")  # 电话可选，默认空
        photo = request.FILES.get("photo")  # 照片文件，可能为None

        # 2. 数据验证（简单验证，实际项目可以用Django表单或序列化器做更严格的验证）
        error_msg = ""
        if not student_id:
            error_msg = "学号不能为空！"
        elif not name:
            error_msg = "姓名不能为空！"
        elif not class_name:
            error_msg = "班级不能为空！"
        elif not age or not age.isdigit():
            error_msg = "年龄必须是数字！"
        # 检查学号是否已存在
        elif Student.objects.filter(student_id=student_id).exists():
            error_msg = "该学号已存在！"

        if error_msg:
            # 验证失败，返回错误信息到前端
            return render(request, "students/student_add.html", {"error_msg": error_msg})

        # 3. 保存数据到数据库
        student = Student(
            student_id=student_id,
            name=name,
            gender=gender,
            class_name=class_name,
            age=int(age),
            phone=phone,
        )
        # 如果有照片，才赋值（否则用默认的null）
        if photo:
            student.photo = photo
        # 保存到数据库
        student.save()

        # 4. 新增成功，重定向到学生列表页
        return redirect("student_list")  # 对应urls.py中的name="student_list"

    # 如果是GET请求，返回新增学生的表单页面
    return render(request, "students/student_add.html")



def student_edit(request, student_id):
    """修改学生信息（接收学号参数）"""
    # 1. 根据学号获取学生对象，如果不存在则返回404错误
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == "POST":
        # 2. 获取前端提交的新数据
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        class_name = request.POST.get("class_name")
        age = request.POST.get("age")
        phone = request.POST.get("phone", "")
        photo = request.FILES.get("photo")  # 新的照片，可能为None

        # 3. 数据验证
        error_msg = ""
        if not name:
            error_msg = "姓名不能为空！"
        elif not class_name:
            error_msg = "班级不能为空！"
        elif not age or not age.isdigit():
            error_msg = "年龄必须是数字！"

        if error_msg:
            return render(request, "students/student_edit.html", {"error_msg": error_msg, "student": student})

        # 4. 更新数据
        student.name = name
        student.gender = gender
        student.class_name = class_name
        student.age = int(age)
        student.phone = phone
        # 如果有新的照片，替换原来的照片（如果没有，保留原来的）
        if photo:
            student.photo = photo
        # 保存更新
        student.save()

        # 5. 修改成功，重定向到学生列表页
        return redirect("student_list")

    # 如果是GET请求，返回修改表单页面，并传递学生原有数据
    return render(request, "students/student_edit.html", {"student": student})


def student_delete(request, student_id):
    """删除学生信息"""
    # 1. 获取学生对象
    student = get_object_or_404(Student, student_id=student_id)
    # 2. 删除学生（物理删除，也可以用逻辑删除：加一个is_delete字段，设置为True）
    student.delete()
    # 3. 重定向到学生列表页
    return redirect("student_list")