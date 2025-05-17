# jtapp/apps.py
from django.db import models

# 定义蔬果模型
class FruitVeggie(models.Model):
    # 蔬果名称，确保唯一性
    name = models.CharField(max_length=100, unique=True, verbose_name="蔬果名称")
    # 含糖量，使用 DecimalField 保证精度
    sugar_content = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="含糖量 (每100克)")
    # 升糖指数，使用 DecimalField
    gi_index = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="升糖指数 (GI)")

    # Meta 类用于设置模型的元数据，例如在 Admin 后台显示的名称
    class Meta:
        verbose_name = "蔬果数据"
        verbose_name_plural = "蔬果数据"

    # 定义对象的字符串表示，方便在 Admin 后台查看
    def __str__(self):
        return self.name

