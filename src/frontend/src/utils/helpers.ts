// 格式化文件大小
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化时间
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 防抖函数
export const debounce = (func: Function, wait: number): Function => {
    let timeout: NodeJS.Timeout | null = null
    return function executedFunction(...args: any[]) {
    const later = () => {
        if (timeout) clearTimeout(timeout)
      func(...args)
    }
        if (timeout) clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 生成随机颜色
export const getRandomColor = (): string => {
  const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
  return colors[Math.floor(Math.random() * colors.length)]
}