# jtapp/urls.py

from django.urls import path
from . import views # 从当前应用导入视图

# 定义 URL 模式
urlpatterns = [
    # 当访问 /search/ 时，调用 views.search_fruit_veggie 函数，并命名为 'search_fruit_veggie'
    path('search/', views.search_fruit_veggie, name='search_fruit_veggie'),
    # 你可以在这里添加其他 URL 模式，例如详细信息页面的路径
]
