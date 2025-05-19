# jtapp/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

# 定义蔬果模型
class FruitVeggie(models.Model):
    CATEGORY_CHOICES = [
        ('vegetable', '蔬菜'),
        ('fruit', '水果'),
    ]
    # 蔬果名称，确保唯一性
    name = models.CharField(max_length=100, verbose_name="名称")
    # 蔬果英文名称
    name_en = models.CharField(max_length=100, verbose_name="英文名称", null=True, blank=True)
    # 蔬果类别 vegetable, fruit
    category = models.CharField('类别', max_length=10, choices=CATEGORY_CHOICES)
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
        return f"{self.name} / {self.name_en}"

