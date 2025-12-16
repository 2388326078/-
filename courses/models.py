from django.db import models

class Course(models.Model):
    """课程信息模型"""
    # 课程编号：主键，唯一标识
    course_id = models.CharField(verbose_name="课程编号", max_length=20, primary_key=True)
    # 课程名称：非空，唯一（避免重复课程名）
    course_name = models.CharField(verbose_name="课程名称", max_length=100, unique=True)
    # 课程描述：可选
    description = models.TextField(verbose_name="课程描述", blank=True, null=True)
    # 创建时间/更新时间
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "courses"
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.course_name}({self.course_id})"
