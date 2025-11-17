<!-- src/views/Payment.vue -->
<template>
  <div class="payment-page">
    <div class="order-info">
      <h2>订单信息</h2>
      <p>商品描述: {{ order.description }}</p>
      <p>订单金额: ¥{{ order.amount }}</p>
    </div>

    <div class="payment-methods">
      <h2>选择支付方式</h2>
      <div class="method-options">
        <button
          :class="['method-btn', { active: selectedMethod === 'alipay' }]"
          @click="selectMethod('alipay')"
        >
          <img src="@/assets/alipay.png" alt="支付宝">
          支付宝支付
        </button>

        <button
          :class="['method-btn', { active: selectedMethod === 'wechat' }]"
          @click="selectMethod('wechat')"
        >
          <img src="@/assets/wechat.png" alt="微信支付">
          微信支付
        </button>
      </div>
    </div>

    <div class="payment-action">
      <button class="pay-btn" @click="handlePayment" :disabled="processing">
        {{ processing ? '处理中...' : `立即支付 ¥${order.amount}` }}
      </button>
    </div>

    <!-- 支付二维码弹窗 -->
    <div v-if="showQRCode" class="qrcode-modal">
      <div class="modal-content">
        <h3>请扫码支付</h3>
        <img :src="qrCodeUrl" alt="支付二维码">
        <p>请使用{{ selectedMethod === 'alipay' ? '支付宝' : '微信' }}扫描二维码完成支付</p>
        <button @click="showQRCode = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import { createPayment, checkPaymentStatus } from '@/api/payment'

export default {
  name: 'PaymentPage',
  data() {
    return {
      selectedMethod: 'alipay',
      processing: false,
      showQRCode: false,
      qrCodeUrl: '',
      order: {
        description: '素材网站VIP会员',
        amount: '99.00'
      },
      currentOrderId: ''
    }
  },
  methods: {
    selectMethod(method) {
      this.selectedMethod = method
    },

    async handlePayment() {
      this.processing = true

      try {
        const paymentData = {
          // user_id: this.$store.state.user.id, // 从Vuex获取用户ID
          amount: this.order.amount,
          description: this.order.description,
          payment_method: this.selectedMethod
        }

        const response = await createPayment(paymentData)
        this.currentOrderId = response.data.order_id

        if (this.selectedMethod === 'alipay') {
          // 支付宝支付 - 跳转到支付页面
          window.location.href = response.data.pay_url
        } else if (this.selectedMethod === 'wechat') {
          // 微信支付 - 显示二维码
          this.handleWechatPayment(response.data.payment_data)
        }
      } catch (error) {
        console.error('支付失败:', error)
        this.$message.error('支付请求失败，请重试')
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
      // 这里应该根据支付数据生成二维码
      // 可以使用qrcode.js库生成二维码
      this.qrCodeUrl = this.generateQRCode(paymentData.pay_url)
      this.showQRCode = true

      // 开始轮询支付状态
      this.pollPaymentStatus()
    },

    async pollPaymentStatus() {
      const checkInterval = setInterval(async () => {
        try {
          const response = await checkPaymentStatus(this.currentOrderId)
          if (response.data.status === 'paid') {
            this.$message.success('支付成功')
            this.showQRCode = false
            clearInterval(checkInterval)
            this.$router.push('/payment/success')
          }
        } catch (error) {
          console.error('检查支付状态失败:', error)
        }
      }, 3000) // 每3秒检查一次
    },

    generateQRCode(url) {
      // 使用二维码生成库生成二维码图片URL
      // 这里返回一个示例URL，实际使用时需要真正生成二维码
      return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`
    }
  }
}
</script>

<style scoped>
.payment-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.order-info, .payment-methods {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.method-options {
  display: flex;
  gap: 15px;
  margin-top: 15px;
}

.method-btn {
  flex: 1;
  padding: 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.method-btn.active {
  border-color: #1890ff;
  background: #f0f8ff;
}

.method-btn img {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}

.pay-btn {
  width: 100%;
  padding: 15px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
}

.pay-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.qrcode-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
}
</style>