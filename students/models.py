from django.db import models

class Student(models.Model):
    """学生信息模型"""
    # 学号：主键，唯一标识，字符类型（避免纯数字的学号前导零丢失）
    student_id = models.CharField(verbose_name="学号", max_length=20, primary_key=True)
    # 姓名：非空
    name = models.CharField(verbose_name="姓名", max_length=50)
    # 性别：可选值为男/女，默认男
    gender_choices = (
        ("男", "男"),
        ("女", "女"),
    )
    gender = models.CharField(verbose_name="性别", max_length=10, choices=gender_choices, default="男")
    # 班级：如“2024级计算机1班”
    class_name = models.CharField(verbose_name="班级", max_length=50)
    # 年龄：正整数
    age = models.PositiveIntegerField(verbose_name="年龄")
    # 电话：可选，允许为空
    phone = models.CharField(verbose_name="电话", max_length=11, blank=True, null=True)
    # 照片：上传到media/student_photos目录，允许为空（blank是前端验证，null是数据库允许空）
    photo = models.ImageField(
        verbose_name="照片",
        upload_to="student_photos/",  # 上传路径：media/student_photos/
        blank=True,
        null=True
    )
    # 创建时间：自动记录创建时间
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    # 更新时间：自动记录更新时间
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        # 数据库表名（可选，默认是应用名_模型名小写）
        db_table = "student"
        # 后台管理显示的名称
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name  # 复数形式和单数一致

    def __str__(self):
        # 打印对象时显示姓名+学号，便于调试
        return f"{self.name}({self.student_id})"
