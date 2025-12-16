from django.db import models
import bcrypt

class User(models.Model):
    """自定义用户模型：替代Django auth的User模型"""
    # 用户名：唯一，作为登录账号
    username = models.CharField(verbose_name="用户名", max_length=50, unique=True)
    # 加密后的密码：存储bcrypt加密后的字节串（转成字符串存储）
    password = models.CharField(verbose_name="密码", max_length=255)
    # 昵称：可选
    nickname = models.CharField(verbose_name="昵称", max_length=50, blank=True, null=True)
    # 登录状态：可选，记录最后登录时间
    last_login = models.DateTimeField(verbose_name="最后登录时间", blank=True, null=True)
    # 创建时间/更新时间
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "custom_user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 自定义方法：加密密码
    def set_password(self, raw_password):
        """
        将原始密码加密后存储
        :param raw_password: 用户输入的原始密码（字符串）
        """
        # 生成盐值（bcrypt会自动生成，也可以手动指定）
        salt = bcrypt.gensalt()
        # 将原始密码转成字节串，然后加密
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        # 把字节串转成字符串存储（因为Django的CharField不支持字节串）
        self.password = hashed_password.decode('utf-8')

    # 自定义方法：验证密码
    def check_password(self, raw_password):
        """
        验证用户输入的原始密码是否与存储的加密密码匹配
        :param raw_password: 用户输入的原始密码（字符串）
        :return: 匹配返回True，否则返回False
        """
        try:
            # 将存储的密码字符串转回字节串，与原始密码字节串对比
            return bcrypt.checkpw(
                raw_password.encode('utf-8'),
                self.password.encode('utf-8')
            )
        except Exception as e:
            # 密码格式错误时返回False
            print(f"密码验证失败：{e}")
            return False