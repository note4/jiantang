import csv
from io import StringIO
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from jtapp.models import FruitVeggie

# CSV导入函数，支持从上传的文件导入数据
def import_fruitveggie_from_file(file: UploadedFile):
    # 将上传文件内容转换为字符串流，默认 utf-8 解码
    text_file = StringIO(file.read().decode('utf-8'))
    reader = csv.DictReader(text_file)
    for row in reader:
        # 按 name 查找，有则更新，无则创建
        FruitVeggie.objects.update_or_create(
            name=row.get('name', '').strip(),
            defaults={
                'name_en': row.get('name_en', '').strip(),
                'sugar_content': float(row.get('sugar_content', 0)),
                'gi_index': float(row.get('gi_index', 0)),
            }
        )

# CSV导出函数，导出给定 queryset，返回 HttpResponse 触发文件下载
def export_fruitveggie_as_csv(queryset, filename):
    # 创建响应对象，告诉浏览器这是一个 CSV 文件下载
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 写入 BOM，告诉 Excel 这是 UTF-8 文件
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    # 写入 CSV 文件头
    writer.writerow(['name', 'name_en', 'sugar_content', 'gi_index'])
    # 写入每一条数据
    for obj in queryset:
        writer.writerow([obj.name, obj.name_en, obj.sugar_content, obj.gi_index])

    return response
