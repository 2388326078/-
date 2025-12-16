from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from functools import wraps
from .models import User

# ---------------------- 权限控制：登录校验装饰器 ----------------------
def login_required(view_func):
    """
    自定义登录校验装饰器：替代Django auth的login_required
    作用：如果用户未登录，跳转到登录页；已登录则执行原视图函数
    """
    @wraps(view_func)  # 保留原函数的名称和文档字符串
    def wrapper(request, *args, **kwargs):
        # 判断session中是否有用户标识（我们用user_id作为标识）
        if 'user_id' not in request.session:
            # 未登录，跳转到登录页，并记录当前页面的URL，方便登录后跳转回来
            return redirect(f"/users/login/?next={request.path}")
        # 已登录，执行原视图函数
        return view_func(request, *args, **kwargs)
    return wrapper

# ---------------------- 核心视图函数 ----------------------
def user_register(request):
    """用户注册：接收用户名和密码，加密后保存到数据库"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        nickname = request.POST.get("nickname", "")

        # 数据验证
        error_msg = ""
        if not username or not password:
            error_msg = "用户名和密码不能为空！"
        elif password != password_confirm:
            error_msg = "两次输入的密码不一致！"
        elif User.objects.filter(username=username).exists():
            error_msg = "用户名已存在！"
        elif len(password) < 6:
            error_msg = "密码长度不能少于6位！"

        if error_msg:
            return render(request, "users/register.html", {"error_msg": error_msg})

        # 保存用户：密码加密
        user = User(username=username, nickname=nickname)
        user.set_password(password)  # 调用自定义的加密方法
        user.save()

        # 注册成功，跳转到登录页
        return redirect("user_login")

    # GET请求：返回注册页面
    return render(request, "users/register.html")

def user_login(request):
    """用户登录：验证账号密码，通过则记录session"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 核心修改：默认跳转地址改为学生列表页
        next_url = request.GET.get("next", "/students/list/")  # 替换原来的"/"

        # 以下原有逻辑不变...
        error_msg = ""
        if not username or not password:
            error_msg = "用户名和密码不能为空！"
        else:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    user.last_login = timezone.now()
                    user.save()
                    return redirect(next_url)  # 登录后跳学生列表
                else:
                    error_msg = "密码错误！"
            except User.DoesNotExist:
                error_msg = "用户名不存在！"

        return render(request, "users/login.html", {"error_msg": error_msg, "username": username})

    return render(request, "users/login.html")

def user_logout(request):
    """用户退出：清除session中的登录状态"""
    # 清除指定的session键
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'username' in request.session:
        del request.session['username']
    # 也可以清除所有session：request.session.flush()
    # 跳转到登录页
    return redirect("user_login")

@login_required  # 应用登录校验装饰器，需要登录才能访问
def user_profile(request):
    """个人中心：展示用户信息（需要登录）"""
    # 从session中获取user_id，查询用户信息
    user = get_object_or_404(User, id=request.session['user_id'])
    return render(request, "users/profile.html", {"user": user})