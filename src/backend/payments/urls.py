# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('notify/<str:payment_method>/', views.PaymentNotifyView.as_view(), name='payment_notify'),
]