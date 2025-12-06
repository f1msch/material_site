// stores/payment.ts
import {defineStore} from 'pinia'
import {createPayment} from '@/api/payment'
import type {CreatePaymentData, PaymentMethod, PaymentOrder} from '@/types'

interface PaymentState {
    selectedMethod: PaymentMethod
    processing: boolean
    showQRCode: boolean
    qrCodeUrl: string
    currentOrderId: string
    currentOrder: PaymentOrder | null
    order: {
        description: string
        amount: string
    }
}


export const usePaymentStore = defineStore('payment', {
    state: (): PaymentState => ({
        selectedMethod: 'alipay',
        processing: false,
        showQRCode: false,
        qrCodeUrl: '',
        currentOrderId: '',
        currentOrder: null,
        order: {
            description: '素材网站VIP会员',
            amount: '99.00'
        }
    }),

    actions: {
        setSelectedMethod(method: PaymentMethod): void {
            this.selectedMethod = method
        },

        setProcessing(status: boolean): void {
            this.processing = status
        },

        setShowQRCode(status: boolean): void {
            this.showQRCode = status
        },

        setQrCodeUrl(url: string): void {
            this.qrCodeUrl = url
        },

        setCurrentOrderId(orderId: string): void {
            this.currentOrderId = orderId
        },

        setCurrentOrder(order: PaymentOrder | null): void {
            this.currentOrder = order
        },

        async createPayment(userId: number | string): Promise<PaymentOrder> {
            this.processing = true

            try {
                const paymentData: CreatePaymentData = {
                    user: userId,
                    amount: parseFloat(this.order.amount),
                    description: this.order.description,
                    plan: 'vip_monthly'
                }

                const response = await createPayment(paymentData)
                this.currentOrderId = response.data.order_id
                this.currentOrder = response.data
                return response.data
            } catch (error) {
                console.error('支付请求失败:', error)
                throw error
            } finally {
                this.processing = false
            }
        },

        handleWechatPayment(paymentData) {
            if (typeof WeixinJSBridge !== 'undefined') {
                // 在微信环境中直接调起支付
                WeixinJSBridge.invoke(
                    'getBrandWCPayRequest',
                    paymentData,
                    (res) => {
                        if (res.err_msg === 'get_brand_wcpay_request:ok') {
                            this.$message.success('支付成功')
                            this.$router.push('/payment/success')
                        } else {
                            this.$message.error('支付取消或失败')
                        }
                    }
                )
            } else {
                // 非微信环境，显示二维码
                this.showWechatQRCode(paymentData)
            }
        },

        showWechatQRCode(paymentData) {
            this.qrCodeUrl = this.generateQRCode(paymentData.pay_url)
            this.showQRCode = true
        },

        generateQRCode(url) {
            // 使用二维码生成库生成二维码图片URL
            return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`
        }
    }
})