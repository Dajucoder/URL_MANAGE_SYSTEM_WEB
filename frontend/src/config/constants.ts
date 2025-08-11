// 默认颜色选项
export const DEFAULT_COLORS = [
  '#1890ff', // 蓝色
  '#52c41a', // 绿色
  '#faad14', // 橙色
  '#f5222d', // 红色
  '#722ed1', // 紫色
  '#fa8c16', // 橙红色
  '#13c2c2', // 青色
  '#eb2f96', // 粉色
  '#666666', // 灰色
  '#000000', // 黑色
];

// 图标选项
export const ICON_OPTIONS = [
  'folder',
  'home',
  'star',
  'heart',
  'book',
  'code',
  'tool',
  'setting',
  'user',
  'team',
  'shop',
  'car',
  'camera',
  'music',
  'video',
  'picture',
  'file',
  'mail',
  'phone',
  'global',
];

// 应用名称
export const APP_NAME = 'URL管理系统';

// API 基础URL
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// 分页配置
export const PAGE_SIZE = 20;

// 文件上传配置
export const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

// 主题配置
export const THEME_COLORS = {
  primary: '#1890ff',
  success: '#52c41a',
  warning: '#faad14',
  error: '#f5222d',
  info: '#1890ff',
};

// 主题选项
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto',
} as const;

export const THEME_OPTIONS = [
  { value: THEMES.LIGHT, label: '浅色主题' },
  { value: THEMES.DARK, label: '深色主题' },
  { value: THEMES.AUTO, label: '跟随系统' },
];

// 语言选项
export const LANGUAGES = {
  ZH_CN: 'zh-CN',
  EN: 'en-US',
  JA: 'ja-JP',
} as const;

export const LANGUAGE_OPTIONS = [
  { value: LANGUAGES.ZH_CN, label: '简体中文' },
  { value: LANGUAGES.EN, label: 'English' },
  { value: LANGUAGES.JA, label: '日本語' },
];

// 错误消息
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  UNAUTHORIZED: '登录已过期，请重新登录',
  FORBIDDEN: '没有权限执行此操作',
  NOT_FOUND: '请求的资源不存在',
  SERVER_ERROR: '服务器内部错误，请稍后重试',
  VALIDATION_ERROR: '数据验证失败',
  UNKNOWN_ERROR: '未知错误，请稍后重试',
};

// 网站状态
export const WEBSITE_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  PENDING: 'pending',
  ERROR: 'error',
};

// 书签类型
export const BOOKMARK_TYPES = {
  WEBSITE: 'website',
  ARTICLE: 'article',
  VIDEO: 'video',
  IMAGE: 'image',
  DOCUMENT: 'document',
  OTHER: 'other',
};
