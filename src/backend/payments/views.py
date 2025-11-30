# payments/views.py
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json
from .models import Order, PaymentTransaction
from .alipay_service import AlipayService
from .wechatpay_service import WeChatPayService


class CreatePaymentView(APIView):
    """创建支付订单"""

    def post(self, request):
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        description = request.data.get('description')
        payment_method = request.data.get('payment_method')

        # 创建订单
        order = Order.objects.create(
            order_id=self.generate_order_id(),
            user_id=user_id,
            amount=amount,
            description=description
        )

        # 根据支付方式调用不同服务
        if payment_method == 'alipay':
            result = self.create_alipay_payment(order)
        elif payment_method == 'wechat':
            result = self.create_wechat_payment(order, request.META.get('REMOTE_ADDR'))
        else:
            return Response({'error': '不支持的支付方式'}, status=status.HTTP_400_BAD_REQUEST)

        if result['success']:
            # 保存支付交易记录
            PaymentTransaction.objects.create(
                order=order,
                payment_method=payment_method,
                prepay_id=result.get('prepay_id', ''),
                payment_data=json.dumps(result.get('payment_data', {}))
            )

            return Response({
                'order_id': order.order_id,
                'payment_data': result.get('payment_data'),
                'pay_url': result.get('pay_url')
            })
        else:
            order.status = 'failed'
            order.save()
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

    def generate_order_id(self):
        """生成订单号"""
        import time
        return f"ORDER{int(time.time())}{random.randint(1000, 9999)}"

    def create_alipay_payment(self, order):
        alipay_service = AlipayService()
        return alipay_service.create_payment(
            order.order_id,
            order.amount,
            order.description
        )

    def create_wechat_payment(self, order, client_ip):
        wechat_service = WeChatPayService()
        return wechat_service.create_unified_order(
            order.order_id,
            order.amount,
            order.description,
            client_ip
        )


class PaymentNotifyView(APIView):
    """支付结果异步通知"""

    def post(self, request, payment_method):
        if payment_method == 'alipay':
            return self.alipay_notify(request)
        elif payment_method == 'wechat':
            return self.wechat_notify(request)
        else:
            return HttpResponse('fail')

    def alipay_notify(self, request):
        alipay_service = AlipayService()
        data = request.POST.dict()

        # 验证签名
        if alipay_service.verify_notify(data):
            order_id = data.get('out_trade_no')
            trade_status = data.get('trade_status')

            try:
                order = Order.objects.get(order_id=order_id)
                if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
                    order.status = 'paid'
                    order.save()

                    # 更新交易记录
                    transaction = PaymentTransaction.objects.get(order=order)
                    transaction.transaction_id = data.get('trade_no')
                    transaction.status = 'paid'
                    transaction.save()

                return HttpResponse('success')
            except Order.DoesNotExist:
                return HttpResponse('fail')
        else:
            return HttpResponse('fail')

    def wechat_notify(self, request):
        wechat_service = WeChatPayService()
        result = wechat_service.xml_to_dict(request.body)

        if result.get('return_code') == 'SUCCESS':
            # 验证签名
            sign = result.pop('sign')
            if wechat_service.generate_sign(result) == sign:
                order_id = result.get('out_trade_no')

                try:
                    order = Order.objects.get(order_id=order_id)
                    if result.get('result_code') == 'SUCCESS':
                        order.status = 'paid'
                        order.save()

                        # 更新交易记录
                        transaction = PaymentTransaction.objects.get(order=order)
                        transaction.transaction_id = result.get('transaction_id')
                        transaction.status = 'paid'
                        transaction.save()

                    # 返回成功响应给微信
                    response_data = {
                        'return_code': 'SUCCESS',
                        'return_msg': 'OK'
                    }
                    return HttpResponse(wechat_service.dict_to_xml(response_data),
                                        content_type='application/xml')
                except Order.DoesNotExist:
                    pass

        # 失败响应
        response_data = {
            'return_code': 'FAIL',
            'return_msg': '处理失败'
        }
        return HttpResponse(wechat_service.dict_to_xml(response_data),
                            content_type='application/xml')