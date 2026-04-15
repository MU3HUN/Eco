from rest_framework import serializers


from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.invoice.models.invoice import InviceInfo

# ================================================= #
# ************** 项目管理 序列化器  ************** #
# ================================================= #
class InviceInfoSerializer(CustomModelSerializer):
    """
    项目管理 简单序列化器
    """

    class Meta:
        model = InviceInfo
        fields = '__all__'


