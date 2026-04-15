from django.conf import settings
from django.db.models import CharField, ForeignKey, CASCADE, SET_NULL,FloatField,DateField,IntegerField


from apps.vadmin.op_drf.models import CoreModel
# 继承框架封装的 模型类 CoreModel
class InviceInfo(CoreModel):
    gongsi = CharField(max_length=50, verbose_name='公司名称')
    number = CharField(max_length=8, verbose_name='发票号码')
    daima = CharField(max_length=8, verbose_name='发票代码')
    amount= CharField(max_length=20, verbose_name='金额')
    ymd = IntegerField(max_length=20, verbose_name='日期')
    json = CharField(max_length=255, verbose_name='返回内容')
    VerifyMessage = CharField(max_length=50, verbose_name='关键信息')
    boolcheck = CharField(max_length=10, verbose_name='是否已验证')
    class Meta:
        verbose_name = '发票管理'
        verbose_name_plural = verbose_name
        ordering = ('boolcheck','number',)
    def __str__(self):
        return f"{self.name} 发票管理"

