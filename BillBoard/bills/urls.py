from django.urls import path
from .views import *

urlpatterns = [
   path('', BillList.as_view(), name='bills'),
   path('<int:pk>', BillDetail.as_view(), name='bill'),
   path('clicks/', ClickList.as_view(), name='clicks'),
   path('click/<int:pk>/', ClickDetail.as_view(), name='click'),
   path('create/', BillCreate.as_view(), name='bill_create'),
   path('<int:pk>/click_create/', ClickCreate.as_view(), name='click_create'),
   path('bill_user/<int:pk>/', BillDetailUser.as_view(), name='bill_user'),
   path('update/<int:pk>', BillUpdate.as_view(), name='bill_update'),
   path('delete/<int:pk>', BillDelete.as_view(), name='bill_delete'),
   path('click_delete/<int:pk>', ClickDelete.as_view(), name='click_delete'),
   path('user_bills/', user_bills, name='user_bills'),
   path('user_clicks/', user_clicks, name='user_clicks'),
   path('accept_click/<int:pk>/', accept_click, name='accept_click'),
]