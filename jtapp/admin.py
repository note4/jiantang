# jtapp/admin.py
from django.contrib import admin
from .models import FruitVeggie

# 注册 FruitVeggie 模型到 Django Admin
# admin.site.register(FruitVeggie)  # 这行已由自定义注册方式取代

# 你也可以自定义 Admin 的显示方式，例如：
class FruitVeggieAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'sugar_content', 'gi_index') # 在列表页显示的字段，包括英文名
    search_fields = ('name', 'name_en') # 添加搜索框，支持中英文名搜索

# 使用自定义的 FruitVeggieAdmin 注册模型
admin.site.register(FruitVeggie, FruitVeggieAdmin)
