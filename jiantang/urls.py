"""
URL configuration for jiantang project.

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
from django.urls import path, include # 导入 include 函数

urlpatterns = [
    # Admin 后台的 URL
    path('admin/', admin.site.urls),
    # 将 dataapp 应用的 URL 包含进来，设置为空路径 '' 表示 dataapp 的 URL 直接挂在网站根目录下
    path('', include('jtapp.urls')),
    # 如果你想让查询页面在 /nutrition/search/ 下，可以改为：
    # path('nutrition/', include('jtapp.urls')),
]
