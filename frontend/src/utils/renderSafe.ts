/**
 * 渲染安全工具函数
 * 用于确保传递给React组件的数据是可渲染的
 */

/**
 * 安全地将任何值转换为可渲染的字符串
 * @param value 任何值
 * @param fallback 默认值
 * @returns 安全的字符串
 */
export const safeRender = (value: any, fallback: string = ''): string => {
  if (value === null || value === undefined) {
    return fallback;
  }
  
  if (typeof value === 'string') {
    return value;
  }
  
  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value);
  }
  
  if (typeof value === 'object') {
    // 如果是对象，尝试获取有意义的属性
    if (value.toString && typeof value.toString === 'function') {
      const stringValue = value.toString();
      // 避免返回 [object Object]
      if (stringValue !== '[object Object]') {
        return stringValue;
      }
    }
    
    // 如果对象有name属性，使用name
    if (value.name && typeof value.name === 'string') {
      return value.name;
    }
    
    // 如果对象有title属性，使用title
    if (value.title && typeof value.title === 'string') {
      return value.title;
    }
    
    // 如果对象有label属性，使用label
    if (value.label && typeof value.label === 'string') {
      return value.label;
    }
    
    // 最后尝试JSON.stringify，但要处理循环引用
    try {
      return JSON.stringify(value);
    } catch (error) {
      console.warn('无法序列化对象:', value, error);
      return fallback;
    }
  }
  
  return String(value);
};

/**
 * 安全地渲染URL
 * @param url URL字符串或对象
 * @returns 安全的URL字符串
 */
export const safeRenderUrl = (url: any): string => {
  const urlString = safeRender(url);
  
  // 基本URL验证
  if (!urlString) return '#';
  
  // 如果不是以http开头，添加https
  if (!urlString.startsWith('http://') && !urlString.startsWith('https://')) {
    return `https://${urlString}`;
  }
  
  return urlString;
};

/**
 * 安全地渲染日期
 * @param date 日期字符串或Date对象
 * @returns 格式化的日期字符串
 */
export const safeRenderDate = (date: any): string => {
  if (!date) return '-';
  
  try {
    const dateObj = new Date(date);
    if (isNaN(dateObj.getTime())) {
      return safeRender(date, '-');
    }
    return dateObj.toLocaleDateString();
  } catch (error) {
    return safeRender(date, '-');
  }
};

/**
 * 安全地渲染数字
 * @param num 数字或字符串
 * @param fallback 默认值
 * @returns 安全的数字字符串
 */
export const safeRenderNumber = (num: any, fallback: string | number = 0): string => {
  if (num === null || num === undefined) {
    return String(fallback);
  }
  
  const parsed = Number(num);
  if (isNaN(parsed)) {
    return String(fallback);
  }
  
  return String(parsed);
};

/**
 * 验证数据是否可以安全渲染
 * @param data 要验证的数据
 * @returns 是否安全
 */
export const isRenderSafe = (data: any): boolean => {
  if (data === null || data === undefined) {
    return true;
  }
  
  const type = typeof data;
  return type === 'string' || type === 'number' || type === 'boolean';
};

/**
 * 深度清理对象，确保所有属性都是可渲染的
 * @param obj 要清理的对象
 * @returns 清理后的对象
 */
export const sanitizeForRender = <T extends Record<string, any>>(obj: T): T => {
  if (!obj || typeof obj !== 'object') {
    return obj;
  }
  
  const sanitized = { ...obj } as any;
  
  Object.keys(sanitized).forEach(key => {
    const value = sanitized[key];
    
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      // 对于嵌套对象，递归清理
      sanitized[key] = sanitizeForRender(value);
    } else if (!isRenderSafe(value)) {
      // 对于不安全的值，转换为安全字符串
      sanitized[key] = safeRender(value);
    }
  });
  
  return sanitized;
};
