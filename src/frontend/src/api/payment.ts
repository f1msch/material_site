import $api from "@/api/index"
import type {CreatePaymentData, PaymentOrder} from '@/types'
import type {AxiosResponse} from 'axios'

export const createPayment = async (paymentData: CreatePaymentData): Promise<AxiosResponse<PaymentOrder>> => {
    return $api({
        url: '/api/payments/create/',
        method: 'post',
        data: paymentData
    })
}

export const checkPaymentStatus = async (orderId: string): Promise<AxiosResponse<{
    status: string;
    order: PaymentOrder
}>> => {
    return $api({
        url: '/api/orders/${orderId}/status/',
        method: 'get',
        data: {orderId: orderId}
    })
}