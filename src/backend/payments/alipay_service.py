# payments/alipay_service.py
from alipay import AliPay
from alipay.utils import AliPayConfig
from django.conf import settings
import os


class AlipayService:
    def __init__(self):
        self.app_id = settings.ALIPAY_APP_ID
        self.app_private_key_string = settings.ALIPAY_APP_PRIVATE_KEY
        self.alipay_public_key_string = settings.ALIPAY_PUBLIC_KEY

        self.alipay = AliPay(
            appid=self.app_id,
            app_private_key_string=self.app_private_key_string,
            alipay_public_key_string=self.alipay_public_key_string,
            sign_type="RSA2",
            debug=settings.DEBUG,  # 沙箱环境设为True
            config=AliPayConfig(timeout=15)
        )

    def create_payment(self, order_id, amount, subject, return_url=None):
        """创建支付宝支付"""
        try:
            # 手机网站支付接口
            order_string = self.alipay.api_alipay_trade_wap_pay(
                out_trade_no=order_id,
                total_amount=float(amount),
                subject=subject,
                return_url=return_url or settings.ALIPAY_RETURN_URL,
                notify_url=settings.ALIPAY_NOTIFY_URL
            )

            # 生成支付URL
            if settings.DEBUG:
                pay_url = f"https://openapi.alipaydev.com/gateway.do?{order_string}"
            else:
                pay_url = f"https://openapi.alipay.com/gateway.do?{order_string}"

            return {
                'success': True,
                'pay_url': pay_url,
                'order_string': order_string
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def verify_notify(self, data):
        """验证支付宝异步通知"""
        signature = data.get('sign')
        data.pop('sign', None)
        data.pop('sign_type', None)

        return self.alipay.verify(data, signature)