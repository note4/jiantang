# jtapp/views.py

from django.shortcuts import render
from .models import FruitVeggie
from django.db.models import Q # 导入 Q 对象，用于复杂的查询条件（这里用不到，但了解一下很好）

# 前台查询视图函数
def search_fruit_veggie(request):
    query = request.GET.get('q') # 从 GET 请求参数中获取查询字符串 'q'
    results = [] # 初始化结果列表

    if query: # 如果用户输入了查询内容
        # 使用 filter 进行查询，name__icontains 表示不区分大小写地包含查询字符串
        results = FruitVeggie.objects.filter(name__icontains=query)
        # 如果需要精确匹配，可以使用 name__iexact=query

    # 渲染 search.html 模板，并将结果和查询字符串传递给模板
    return render(request, 'dataapp/search.html', {'results': results, 'query': query})

