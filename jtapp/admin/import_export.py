# jtapp/admin/import_export.py
import csv
from io import StringIO
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from jtapp.models import FruitVeggie

# CSV导入函数，支持从上传的文件导入数据
def import_fruitveggie_from_file(file: UploadedFile):
    # 检测文件是否包含 BOM 头
    content = file.read()
    if content.startswith(b'\xef\xbb\xbf'):
        # 如果有 BOM 头，跳过它
        content = content[3:]
    
    text_file = StringIO(content.decode('utf-8'))
    reader = csv.DictReader(text_file)
    
    # 用于记录导入的数量
    imported_count = 0
    
    try:
        for row in reader:
            try:
                FruitVeggie.objects.update_or_create(
                    name=row.get('name', '').strip(),
                    defaults={
                        'name_en': row.get('name_en', '').strip(),
                        'category': row.get('category', '').strip(),  # 如果是字符串
                        'sugar_content': float(row.get('sugar_content', 0)),
                        'gi_index': float(row.get('gi_index', 0)),
                    }
                )
                imported_count += 1
            except Exception as e:
                # 记录具体哪一行出错
                print(f"Error importing row {imported_count + 1}: {str(e)}")
                continue
        
        return imported_count
    finally:
        text_file.close()

# CSV导出函数，导出给定 queryset，返回 HttpResponse 触发文件下载
def export_fruitveggie_as_csv(queryset, filename):
    # 创建响应对象，告诉浏览器这是一个 CSV 文件下载
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 写入 BOM，告诉 Excel 这是 UTF-8 文件
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    # 写入 CSV 文件头
    writer.writerow(['name', 'name_en', 'category',  'sugar_content', 'gi_index'])
    # 写入每一条数据
    for obj in queryset:
        writer.writerow([obj.name, obj.name_en, obj.category, obj.sugar_content, obj.gi_index])

    return response
