// src/api/payment.js
import request from '@/services/api'
import $api from "@/services/api";

export function createPayment(data) {
  return $api({
    url: '/api/payments/create/',
    method: 'post',
    data
  })
}

export function checkPaymentStatus(orderId) {
  return $api({
    url: `/api/orders/${orderId}/status/`,
    method: 'get'
  })
}