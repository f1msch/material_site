<!-- src/views/PaymentResult.vue -->
<template>
  <div class="payment-result">
    <div class="result-content">
      <div v-if="status === 'success'" class="success">
        <i class="icon-success">✓</i>
        <h2>支付成功</h2>
        <p>感谢您的购买，订单已处理完成</p>
      </div>

      <div v-else-if="status === 'failed'" class="failed">
        <i class="icon-failed">✗</i>
        <h2>支付失败</h2>
        <p>支付过程中出现问题，请重试</p>
      </div>

      <div v-else class="processing">
        <i class="icon-processing">⏳</i>
        <h2>支付处理中</h2>
        <p>请稍候，正在确认支付结果...</p>
      </div>

      <div class="action-buttons">
        <button @click="$router.push('/orders')" class="btn-primary">
          查看订单
        </button>
        <button @click="$router.push('/')" class="btn-secondary">
          返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { checkPaymentStatus } from '@/api/payment'

export default {
  name: 'PaymentResult',
  data() {
    return {
      status: 'processing' // processing, success, failed
    }
  },
  async mounted() {
    const orderId = this.$route.query.order_id
    if (orderId) {
      await this.checkStatus(orderId)
    }
  },
  methods: {
    async checkStatus(orderId) {
      try {
        const response = await checkPaymentStatus(orderId)
        this.status = response.data.status === 'paid' ? 'success' : 'failed'
      } catch (error) {
        this.status = 'failed'
      }
    }
  }
}
</script>