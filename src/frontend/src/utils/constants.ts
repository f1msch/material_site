export const MATERIAL_TYPES = {
  image: '图片',
  vector: '矢量图',
  video: '视频',
  audio: '音频',
  template: '模板',
  font: '字体',
  other: '其他'
}

export const LICENSE_TYPES = {
  free: '免费',
  premium: '付费',
  'cc-by': 'CC BY',
  'cc-by-sa': 'CC BY-SA'
}

export const FILE_ACCEPT_TYPES = {
  image: 'image/*',
  vector: '.svg,.ai,.eps',
  video: 'video/*',
  audio: 'audio/*',
  template: '.psd,.xd,.sketch',
  font: '.ttf,.otf,.woff,.woff2',
  other: '*'
}

export const MAX_FILE_SIZE = 100 * 1024 * 1024 // 100MB