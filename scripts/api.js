/**
 * 极趣实验室 API 调用脚本
 * 使用前请配置你的 API_KEY 和默认 MAC 地址
 */

// ============ 在这里配置你的凭证 ============
const API_KEY = "你的APIKey";      // 替换为你的API Key
const DEFAULT_MAC = "AA:BB:CC:DD:EE:FF";  // 替换为你的设备MAC地址
// ============================================

const BASE_URL = 'https://cloud.zectrix.com/open/v1';

async function apiCall(endpoint, paramsOrData = {}, method = 'GET') {
  const isGet = method === 'GET';
  const url = new URL(`${BASE_URL}/${endpoint}`);
  
  const options = {
    method,
    headers: {
      'X-API-Key': API_KEY
    }
  };

  if (!isGet && method !== 'DELETE') {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(paramsOrData);
  } else if (isGet && typeof paramsOrData === 'object' && Object.keys(paramsOrData).length > 0) {
    Object.entries(paramsOrData).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, value);
      }
    });
  }

  const response = await fetch(url.toString(), options);
  const result = await response.json();
  
  if (result.code !== 0) {
    throw new Error(result.msg || `API Error: ${result.code}`);
  }
  
  return result.data;
}

// 封装好的API方法
const jiquApi = {
  // 获取设备列表
  getDevices: () => apiCall('devices'),
  
  // 获取待办列表
  getTodos: (params = {}) => apiCall('todos', params),
  
  // 创建待办 - 自动关联到默认设备
  createTodo: (data) => {
    // 自动带上 deviceId，使用配置的默认 MAC
    const dataWithDevice = {
      ...data,
      deviceId: data.deviceId || DEFAULT_MAC
    };
    return apiCall('todos', dataWithDevice, 'POST');
  },
  
  // 更新待办
  updateTodo: (id, data) => apiCall(`todos/${id}`, data, 'PUT'),
  
  // 标记完成
  completeTodo: (id) => apiCall(`todos/${id}/complete`, {}, 'PUT'),
  
  // 取消完成
  uncompleteTodo: (id) => apiCall(`todos/${id}/uncomplete`, {}, 'PUT'),
  
  // 删除待办
  deleteTodo: (id) => apiCall(`todos/${id}`, {}, 'DELETE'),
  
  // 推送文本到设备
  pushText: (deviceId, data) => apiCall(`devices/${deviceId}/display/text`, data, 'POST'),
  
  // 推送图片（FormData方式）
  pushImage: (deviceId, formData) => fetch(`${BASE_URL}/devices/${deviceId}/display/image`, {
    method: 'POST',
    headers: { 'X-API-Key': API_KEY },
    body: formData
  }).then(r => r.json())
};

// 导出
module.exports = { apiCall, jiquApi, DEFAULT_MAC };
