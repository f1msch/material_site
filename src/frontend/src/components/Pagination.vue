<template>
  <div class="pagination" v-if="total > 0">
    <button
      class="pagination-btn"
      :disabled="current === 1"
      @click="handlePageChange(current - 1)"
    >
      上一页
    </button>

    <div class="pagination-pages">
      <button
        v-for="page in visiblePages"
        :key="page"
        class="pagination-page"
        :class="{ active: page === current }"
        @click="handlePageChange(page)"
      >
        {{ page }}
      </button>

      <span v-if="showEllipsis" class="pagination-ellipsis">...</span>

      <button
        v-if="showLastPage"
        class="pagination-page"
        :class="{ active: totalPages === current }"
        @click="handlePageChange(totalPages)"
      >
        {{ totalPages }}
      </button>
    </div>

    <button
      class="pagination-btn"
      :disabled="current === totalPages"
      @click="handlePageChange(current + 1)"
    >
      下一页
    </button>

    <div class="pagination-info">
      第 {{ current }} 页，共 {{ totalPages }} 页（{{ total }} 条记录）
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  current: {
    type: Number,
    required: true,
    default: 1
  },
  total: {
    type: Number,
    required: true,
    default: 0
  },
  pageSize: {
    type: Number,
    default: 12
  }
})

const emit = defineEmits(['change'])

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, props.current - 2)
  const end = Math.min(totalPages.value, props.current + 2)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

const showEllipsis = computed(() => {
  return visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1
})

const showLastPage = computed(() => {
  return visiblePages.value[visiblePages.value.length - 1] < totalPages.value
})

const handlePageChange = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    emit('change', page)
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.pagination-pages {
  display: flex;
  gap: 0.5rem;
}

.pagination-btn,
.pagination-page {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled),
.pagination-page:hover:not(.active) {
  background: #f8f9fa;
  border-color: #3498db;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-page.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.pagination-ellipsis {
  padding: 0.5rem;
  color: #6c757d;
}

.pagination-info {
  color: #6c757d;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 0.5rem;
  }

  .pagination-info {
    order: -1;
  }
}
</style>