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
        <button @click="closeQRCodeModal">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePaymentStore } from '@/stores/payment'
import { checkPaymentStatus } from '@/api/payment'
import {useUserStore} from "@/stores/user.js";

const router = useRouter()
const paymentStore = usePaymentStore()
const userStore = useUserStore()

// 使用store中的状态
const selectedMethod = computed(() => paymentStore.selectedMethod)
const processing = computed(() => paymentStore.processing)
const showQRCode = computed(() => paymentStore.showQRCode)
const qrCodeUrl = computed(() => paymentStore.qrCodeUrl)
const order = computed(() => paymentStore.order)

let pollInterval = null

// 方法
const selectMethod = (method) => {
  paymentStore.setSelectedMethod(method)
}

const handlePayment = async () => {
  try {
    // 假设从用户store获取用户ID
    const userId = userStore.user
    const paymentData = await paymentStore.createPayment(userId)

    if (selectedMethod.value === 'alipay') {
      // 支付宝支付 - 跳转到支付页面
      window.location.href = paymentData.pay_url
    } else if (selectedMethod.value === 'wechat') {
      // 微信支付 - 显示二维码或调起微信支付
      paymentStore.handleWechatPayment(paymentData.payment_data)

      // 如果是显示二维码，开始轮询支付状态
      if (paymentStore.showQRCode) {
        startPollingPaymentStatus()
      }
    }
  } catch (error) {
    console.error('支付失败:', error)
    // 这里可以使用UI框架的消息提示
    alert('支付请求失败，请重试')
  }
}

const startPollingPaymentStatus = () => {
  pollInterval = setInterval(async () => {
    try {
      const response = await checkPaymentStatus(paymentStore.currentOrderId)
      if (response.data.status === 'paid') {
        // 支付成功
        alert('支付成功')
        closeQRCodeModal()
        clearInterval(pollInterval)
        router.push('/payment/success')
      }
    } catch (error) {
      console.error('检查支付状态失败:', error)
    }
  }, 3000) // 每3秒检查一次
}

const closeQRCodeModal = () => {
  paymentStore.setShowQRCode(false)
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

// 生命周期
onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})
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