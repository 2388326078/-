"""
URL configuration for student_info_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # 导入重定向视图

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('scores/', include('scores.urls')),
    path('analysis/', include('analysis.urls')),
    path('users/', include('users.urls')),
    # 核心修改：根路径重定向到登录页（替代原来的user_profile）
    path('', RedirectView.as_view(url='/users/login/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)