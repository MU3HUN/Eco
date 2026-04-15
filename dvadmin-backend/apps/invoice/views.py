import os
import shutil
from urllib.request import Request

from django.http import HttpResponse

from apps.invoice.filters import InviceFilter
from apps.invoice.models import InviceInfo
from apps.invoice.serializers import InviceInfoSerializer
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.response import SuccessResponse, SuccessJsonResponse, ErrorResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission
from apps.invoice.utils.paddleOrcHelp import runOrc
from apps.invoice.utils.baiduinvoiceHelp import check,getToken
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage

from django.utils import timezone #引入timezone模块
from django.db.models import Q

class InviceModelViewSet(CustomModelViewSet):
    """
    发票管理 的CRUD视图
    """
    queryset = InviceInfo.objects.all()
    serializer_class = InviceInfoSerializer  # 序列化器

    filter_class = InviceFilter  # 过滤器
    extra_filter_backends = [DataLevelPermissionsFilter]  # 数据权限类，不需要可注释掉
    update_extra_permission_classes = (CommonPermission,)  # 判断用户是否有这条数据的权限
    destroy_extra_permission_classes = (CommonPermission,)  # 判断用户是否有这条数据的权限
    create_extra_permission_classes = (CommonPermission,)  # 判断用户是否有这条数据的权限
    search_fields = ('number',)  # 搜索
    ordering = ['create_datetime']  # 默认排序



    # 通过orc识别图片信息保存到数据库
    def AddinvoinceInfoByOrc(self, request: Request):
        rootdir = 'E:\InvoicePics'
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(rootdir, list[i])
            if os.path.isfile(path):
                # 你想对文件的操作
                try:
                    invoinceinfoModel = InviceInfo();
                    modelByorc = runOrc(invoinceinfoModel, path);
                    invoinceinfoModel.number = modelByorc[0];
                    invoinceinfoModel.daima = modelByorc[1];
                    invoinceinfoModel.ymd = modelByorc[2];
                    invoinceinfoModel.amount = modelByorc[3];
                    invoinceinfoModel.gongsi = modelByorc[4];
                    invoinceinfoModel.boolcheck = '0';
                    invoinceinfoModel.save();
                except:
                    print(modelByorc[0]+"错误")
                #InviceInfo.objects.get_or_create(number=modelByorc[0],daima=modelByorc[1],ymd=modelByorc[2],amount=modelByorc[3]);
        return SuccessResponse(msg="添加成功")
    # 删除发票数据
    def Delinvoince(self,request: Request, *args, **kwargs):
        delids= kwargs.get('pk').split(',')
        if delids:
            InviceInfo.objects.filter(id__in=delids).delete()
        return SuccessResponse(msg="删除成功")


    # 开始调用百度接口进行发票验真，将返回信息保存到数据库
    def Checkinvoince(self, request: Request, *args, **kwargs):
        ids =  kwargs.get('ids').split(',')
        InvoiceInfoList=InviceInfo.objects.filter(id__in=ids)
        if(InvoiceInfoList.count()>0):
            access_token=getToken();
            for f in InvoiceInfoList:
                returnjson=check(f.daima,f.ymd,f.number,f.amount,'special_vat_invoice',access_token);
                #returnjson={'InvoiceDate': '20220211', 'VerifyMessage': '所查发票不存在', 'words_result': {'CommodityAmount': [], 'CarrierCode': '', 'CommodityNum': [], 'SenderCode': '', 'Carrier': '', 'VehicleTypeNum': '', 'TaxControlNum': '', 'PurchaserRegisterNum': '', 'TotalTax': '', 'CommodityVehicleType': [], 'CommodityTaxRate': [], 'SellerAddress': '', 'CommodityEndDate': [], 'CommodityPrice': [], 'Checker': '', 'CommodityType': [], 'Receiver': '', 'CommodityExpenseItem': [], 'RecipientCode': '', 'PurchaserName': '', 'Sender': '', 'SellerRegisterNum': '', 'TransportCargoInformation': '', 'CommodityPlateNum': [], 'TotalAmount': '6406.21', 'SellerBank': '', 'PurchaserAddress': '', 'Payee': '', 'Remarks': '', 'CommodityName': [], 'AmountInFiguers': '', 'NoteDrawer': '', 'DepartureViaArrival': '', 'TollSign': '', 'Recipient': '', 'VehicleTonnage': '', 'PurchaserBank': '', 'ReceiverCode': '', 'CommodityUnit': [], 'CommodityStartDate': [], 'CommodityTax': [], 'SellerName': '', 'ZeroTaxRateIndicator': ''}, 'InvoiceNum': '80996618', 'MachineCode': '', 'words_result_num': 43, 'CheckCode': '', 'VerifyResult': '0009', 'InvoiceCode': '3200211130', 'VerifyFrequency': '', 'InvoiceType': '增值税专用发票', 'InvalidSign': '', 'log_id': 1484341644459867644};
                try:
                    VerifyMessage=returnjson["VerifyMessage"];
                    print(VerifyMessage)
                    updatedatetime = timezone.now()
                    InviceInfo.objects.filter(number=f.number).update(json=returnjson, VerifyMessage=VerifyMessage,
                                                                      boolcheck='1', update_datetime=updatedatetime)
                except:
                    print(returnjson)
        return SuccessResponse(msg="验证完成")

    # 获取发票数据列表（前端调用）
    def get_AllinvoiceList(self, request: Request):
        Querygongsi=request.GET.get('gongsi')
        #invoiceInfoList = InviceInfo.objects.all();
        if Querygongsi==None:
            query = Q()
        else:
            query = Q(gongsi__contains =Querygongsi );
        QuerystartDate = request.GET.get('startDate')
        QueryendDate = request.GET.get('endDate')
        if QuerystartDate == None:
            queryDate = Q()
        else:
            QuerystartDate=QuerystartDate.replace('-','');
            QueryendDate = QueryendDate.replace('-', '');
            int(QuerystartDate)
            int(QueryendDate)
            queryDate = Q(ymd__gte=QuerystartDate,ymd__lte=QueryendDate);

        Queryboolcheck = request.GET.get('boolcheck')
        if Queryboolcheck == None:
            Qboolcheck = Q()
        else:
            if Queryboolcheck=='-1':
                Qboolcheck = Q()
            else:
                Qboolcheck = Q(boolcheck=Queryboolcheck);
        QueryVerifyMessage = request.GET.get('VerifyMessage')
        if QueryVerifyMessage == None:
            QVerifyMessage = Q()
        else:
            if QueryVerifyMessage=='-1':
                QVerifyMessage = Q()
            else:
                QVerifyMessage = Q(VerifyMessage=QueryVerifyMessage);
        invoiceInfoList = InviceInfo.objects.filter(query).filter(queryDate).filter(Qboolcheck).filter(QVerifyMessage);
        pageSize = request.GET.get('pageSize')
        # 创建分页器：每页N条记录
        paginator = Paginator(invoiceInfoList, pageSize)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('pageNum')
        try:
            list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            list = paginator.page(paginator.num_pages)

        # for item in InvoiceInfoList:
        #     print(item.number)
        serializer = InviceInfoSerializer(list, many=True)
        return SuccessResponse(data={"list":serializer.data,"total":invoiceInfoList.count()})

    # 修改发票信息
    def editinvoice(self, request: Request, *args, **kwargs):
        InviceInfo.objects.filter(id=request.data.get('id')).update(number=request.data.get('number'),
                                                                    daima=request.data.get('daima'),
                                                                    amount=request.data.get('amount'),
                                                                    ymd=request.data.get('ymd'),
                                                                    boolcheck='0',
                                                                    VerifyMessage=''
                                                                    )
        return SuccessResponse()

    # 手动添加发票信息
    def addinvoice(self, request: Request, *args, **kwargs):
        invoinceinfoModel = InviceInfo();
        invoinceinfoModel.number = request.data.get('number');
        invoinceinfoModel.daima = request.data.get('daima');
        invoinceinfoModel.ymd = request.data.get('ymd');
        invoinceinfoModel.amount =request.data.get('amount');
        invoinceinfoModel.gongsi = request.data.get('gongsi');
        invoinceinfoModel.boolcheck='0';
        invoinceinfoModel.save()
        return SuccessResponse()

    def del_file(self, request: Request, *args, **kwargs):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 路径
        :return:
        """
        filepath="E:\InvoicePics"
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        return SuccessResponse()