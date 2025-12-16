from django.db import models
from students.models import Student
from courses.models import Course

class Score(models.Model):
    """成绩信息模型"""
    # 成绩ID：自增主键（也可以用复合主键，这里用自增更简单）
    id = models.AutoField(verbose_name="成绩ID", primary_key=True)
    # 学生：外键关联学生表，级联删除（学生删除时，成绩也删除）
    student = models.ForeignKey(
        verbose_name="学生",
        to=Student,
        on_delete=models.CASCADE,
        related_name="scores"  # 反向关联：student.scores可以获取该学生的所有成绩
    )
    # 课程：外键关联课程表，级联删除
    course = models.ForeignKey(
        verbose_name="课程",
        to=Course,
        on_delete=models.CASCADE,
        related_name="scores"
    )
    # 成绩：浮点型，范围0-100
    score = models.FloatField(verbose_name="成绩")
    # 考试时间：可选
    exam_time = models.DateField(verbose_name="考试时间", blank=True, null=True)
    # 创建时间/更新时间
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "score"
        verbose_name = "成绩信息"
        verbose_name_plural = verbose_name
        # 关键：设置联合唯一约束，确保一个学生一门课只有一条记录（数据库层面的校验，双重保障）
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}：{self.score}"
