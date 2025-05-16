
from django.contrib import admin
from .models import FruitVeggie

# 注册 FruitVeggie 模型到 Django Admin
admin.site.register(FruitVeggie)

# 你也可以自定义 Admin 的显示方式，例如：
# class FruitVeggieAdmin(admin.ModelAdmin):
#     list_display = ('name', 'sugar_content', 'gi_index') # 在列表页显示的字段
#     search_fields = ('name',) # 添加搜索框，按名称搜索

# admin.site.register(FruitVeggie, FruitVeggieAdmin)