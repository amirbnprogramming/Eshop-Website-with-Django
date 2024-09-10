from datetime import time

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from order_module.models import Order, OrderDetail
from product_module.models import Product

import requests
import json

# Create your views here.


MERCHANT = 'test'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'



def add_product_to_order(request: HttpRequest) -> HttpResponse:
    product_id = request.GET.get('product_id')
    requested_counter = int(request.GET.get('requested_count'))
    if requested_counter < 1:
        requested_counter = 1
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'تعداد محصول وارد شده صحیح نیست !',
            'icon': 'error',
            'confirm_button_text': 'فهمیدم',
            'cancel_button': False,
            'cancel_button_text': '',
        })

    # check authentication of user
    if request.user.is_authenticated:
        current_user_id = request.user.id
        requested_product = Product.objects.filter(id=product_id, is_active=True, is_deleted=False).first()
        # check if there is product with this considered detail
        if requested_product is not None:
            # get current user open cart or create if it does not have open cart
            # get or create return a tuple (Order, created:bool)
            current_order, created = Order.objects.get_or_create(user_id=current_user_id, is_paid=False)
            # check if the product is in cart or not ; if there is , the count will be increase
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:  # add order_detail
                current_order_detail.count = current_order_detail.count + requested_counter
                current_order_detail.save()
            else:  # create order_detail
                new_order_detail = OrderDetail(product_id=product_id, order_id=current_order.id,
                                               count=requested_counter)
                # add product to its open cart
                new_order_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول موردن نظر با موفقیت به سبد خرید شما اضافه شد',
                'icon': 'success',
                'confirm_button_text': 'فهمیدم',
                'cancel_button': False,
                'cancel_button_text': '',
            })

        else:
            return JsonResponse({
                'status': 'product not found',
                'text': 'محصول مدنظر یافت نشد!',
                'icon': 'error',
                'confirm_button_text': 'محصول دیگری را امتحان کنید',
                'cancel_button_show': False,
                'cancel_button_text': '',
            })

    else:
        return JsonResponse({
            'status': 'not logged in',
            'text': 'برای خرید محصول باید در سایت عضو باشید',
            'icon': 'error',
            'confirm_button_text': 'ورود به سایت',
            'cancel_button': False,
            'cancel_button_text': '',
        })

@login_required
def request_payment(request: HttpRequest):
    current_user_id = request.user.id
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=current_user_id)
    total_price = current_order.get_order_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

@login_required
def verify_request(request: HttpRequest, authority):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                ref_str = req.json()['data']['ref_id']
                return render(request, 'order_module/templates/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'order_module/templates/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'order_module/templates/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'order_module/templates/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order_module/templates/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })
