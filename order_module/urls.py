from django.urls import path
from . import views

urlpatterns= [
    path('add_to_order',views.add_product_to_order,name= 'add-product-to-order'),
    # path('request-payment/', views.send_request_payment(), name='send_request_payment'),
    # path('verify-payment/', views.verify_payment(), name='verify+payment'),
]