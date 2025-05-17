# jtapp/views.py

from django.shortcuts import render
from .models import FruitVeggie
from django.db.models import Q # 导入 Q 对象，用于复杂的查询条件（这里用不到，但了解一下很好）

        
# 首页图片识别
def index(request):
    return render(request, 'dataapp/index.html')


# 前台查询视图函数
def search_fruit_veggie(request):
    query = request.GET.get('q') # 从 GET 请求参数中获取查询字符串 'q'
    results = [] # 初始化结果列表

    if query: # 如果用户输入了查询内容
        # 使用 filter 进行查询，Q 对象实现对中文名和英文名的模糊匹配
        results = FruitVeggie.objects.filter(
            Q(name__icontains=query) | Q(name_en__icontains=query)
        )
        # 如果需要精确匹配，可以使用 name__iexact=query 或 name_en__iexact=query

    # 渲染 search.html 模板，并将结果和查询字符串传递给模板
    return render(request, 'dataapp/search.html', {
        'results': results,
        'query': query
    })



from django.http import JsonResponse
import json
import os

def get_labels(request):
    try:
        labels_path = os.path.join(os.path.dirname(__file__), 'data', 'fruit_labels.json')
        with open(labels_path, 'r', encoding='utf-8') as f:
            labels = json.load(f)
        return JsonResponse(labels)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

        

from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect

def set_language(request):
    lang = request.GET.get('lang', settings.LANGUAGE_CODE)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if lang in dict(settings.LANGUAGES):
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return response


