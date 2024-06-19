from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from order_module.models import Order, OrderDetails
from product_module.models import Product
from django.conf import settings
import requests
import json

#? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8525/orders/verify/'
#
#
# def send_request_payment(request : HttpRequest):
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     total_price = current_order.calculate_total_price()
#     if total_price == 0:
#         return redirect(reverse('user_basket_page'))
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": total_price * 10,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                         'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
#
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}
#
#
# def verify_payment(request : HttpRequest):
#
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response



def add_product_to_order(request : HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'not_accept',
            'text': 'this value not accepted',
            'icon': 'warning',
            'confirmButtonText': 'بله متوجه شدم'
        })
    if request.user.is_authenticated:
        product= Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetails_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetails(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()

            return JsonResponse({'status':'success',
                                 'text': 'با موفقیت اضافه شد',
                                 'icon': 'success',
                                 'confirmButtonText': 'ممنون'
                                 })
        else:
            return JsonResponse({'status':'not_found',
                                 'text': 'محصول وجود ندارد',
                                 'icon': 'warning',
                                 'confirmButtonText': 'بله متوجه شدم'
                                 })

    return JsonResponse({'status': 'not_auth',
                         'text': 'ابتدا باید وارد سایت شوید',
                         'icon': 'warning',
                         'confirmButtonText': 'بله متوجه شدم'
                         })


