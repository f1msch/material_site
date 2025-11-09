<template>
  <div class="upload-progress" v-if="isUploading">
    <div class="progress-header">
      <h3>上传进度</h3>
      <span>{{ progress }}%</span>
    </div>

    <div class="progress-bar">
      <div
        class="progress-fill"
        :style="{ width: progress + '%' }"
      ></div>
    </div>

    <div class="progress-info">
      <p>正在上传文件，请勿关闭页面...</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isUploading: {
    type: Boolean,
    default: false
  },
  progress: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.upload-progress {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-bottom: 2rem;
  border-left: 4px solid #3498db;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.progress-header h3 {
  margin: 0;
  color: #2c3e50;
}

.progress-header span {
  font-weight: 600;
  color: #3498db;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-info {
  margin-top: 0.5rem;
}

.progress-info p {
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
}
</style>