from django.urls import re_path
from rest_framework.routers import DefaultRouter


from apps.invoice.views import InviceModelViewSet
router = DefaultRouter()
router.register(r'invoice', InviceModelViewSet)

urlpatterns = [
    re_path('invoice/AddinvoinceInfoByOrc/', InviceModelViewSet.as_view({'get': 'AddinvoinceInfoByOrc', })),
    re_path('invoice/Checkinvoince/(?P<ids>.*)/', InviceModelViewSet.as_view({'get': 'Checkinvoince', })),
    re_path('invoice/Delinvoince/(?P<pk>.*)/', InviceModelViewSet.as_view({'delete': 'Delinvoince', })),
    re_path('invoice/get_AllinvoiceList', InviceModelViewSet.as_view({'get': 'get_AllinvoiceList', })),
    re_path('invoice/editinvoice/', InviceModelViewSet.as_view({'put': 'editinvoice'})),
    re_path('invoice/addinvoice/', InviceModelViewSet.as_view({'post': 'addinvoice'})),
    re_path('invoice/delfile/', InviceModelViewSet.as_view({'post': 'del_file'})),
]

urlpatterns += router.urls