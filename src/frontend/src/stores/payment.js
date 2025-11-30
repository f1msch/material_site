// stores/payment.js
import { defineStore } from 'pinia'

export const usePaymentStore = defineStore('payment', {
  state: () => ({
    selectedMethod: 'alipay',
    processing: false,
    showQRCode: false,
    qrCodeUrl: '',
    currentOrderId: '',
    order: {
      description: '素材网站VIP会员',
      amount: '99.00'
    }
  }),

  actions: {
    setSelectedMethod(method) {
      this.selectedMethod = method
    },

    setProcessing(status) {
      this.processing = status
    },

    setShowQRCode(status) {
      this.showQRCode = status
    },

    setQrCodeUrl(url) {
      this.qrCodeUrl = url
    },

    setCurrentOrderId(orderId) {
      this.currentOrderId = orderId
    },

    async createPayment(userId) {
      this.processing = true

      try {
        const paymentData = {
          user_id: userId,
          amount: this.order.amount,
          description: this.order.description,
          payment_method: this.selectedMethod
        }

        const response = await createPayment(paymentData)
        this.currentOrderId = response.data.order_id
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