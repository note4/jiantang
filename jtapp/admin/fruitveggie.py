# jtapp/admin/fruitveggie.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms

from jtapp.models import FruitVeggie
from .import_export import import_fruitveggie_from_file, export_fruitveggie_as_csv

from django.utils.translation import gettext_lazy as _

class UploadFileForm(forms.Form):
    # 上传表单，支持 CSV 或 Excel
    file = forms.FileField(label="上传 CSV 或 Excel 文件")


@admin.register(FruitVeggie)
class FruitVeggieAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'category', 'sugar_content', 'gi_index')
    search_fields = ('name', 'name_en')
    list_filter = ('category',)  # 添加类别筛选
    actions = ['export_selected_as_csv']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # 自定义导入页面 URL
            path('import/', self.admin_site.admin_view(self.import_data), name='fruitveggie-import'),
            # 自定义导出所有数据 URL
            path('export-all/', self.admin_site.admin_view(self.export_all_as_csv), name='fruitveggie-export-all'),
        ]
        return custom_urls + urls

    def import_data(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                # 使用导入函数处理上传文件
                import_fruitveggie_from_file(request.FILES['file'])
                self.message_user(request, "数据导入成功！")
                return HttpResponseRedirect("../")  # 导入后跳回列表页
        else:
            form = UploadFileForm()
        return render(request, "admin/import_fruitveggie.html", {"form": form})

    def export_selected_as_csv(self, request, queryset):
        # 导出选中数据为 CSV
        return export_fruitveggie_as_csv(queryset, "selected_fruitveggies.csv")
    export_selected_as_csv.short_description = "导出选中数据为 CSV"

    def export_all_as_csv(self, request):
        # 导出全部数据为 CSV
        return export_fruitveggie_as_csv(FruitVeggie.objects.all(), "all_fruitveggies.csv")

    def changelist_view(self, request, extra_context=None):
        # 在列表页额外传入按钮链接
        if extra_context is None:
            extra_context = {}
        extra_context["custom_buttons"] = [
            {"label": "导入数据", "url": "import/"},
            {"label": "导出全部数据", "url": "export-all/"}
        ]
        return super().changelist_view(request, extra_context=extra_context)
