# jtapp/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# 定义 URL 模式
urlpatterns = [

    path('api/labels/', views.get_labels, name='get_labels'), # 缓存模型名称映射
    path('', views.index, name='index'),  # 添加首页路由
    # 当访问 /search/ 时，调用 views.search_fruit_veggie 函数，并命名为 'search_fruit_veggie'
    path('search/', views.search_fruit_veggie, name='search_fruit_veggie'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)