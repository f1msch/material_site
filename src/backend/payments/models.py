# payments/models.py
from django.db import models
from django.utils import timezone


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('cancelled', '已取消'),
    )

    order_id = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    user_id = models.IntegerField(verbose_name="用户ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    description = models.CharField(max_length=200, verbose_name="商品描述")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentTransaction(models.Model):
    PAYMENT_METHOD = (
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    transaction_id = models.CharField(max_length=128, blank=True, verbose_name="支付平台交易号")
    prepay_id = models.CharField(max_length=128, blank=True, verbose_name="预支付ID")
    payment_data = models.TextField(blank=True, verbose_name="支付参数")
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(default=timezone.now)