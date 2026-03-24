---
name: jiqu-lab-api
description: |
  极趣实验室设备API技能。用于控制极趣实验室智能设备的待办事项和显示屏推送。
  当用户提到以下任一场景时使用：
  1. 待办事项管理：添加待办、查看待办、更新待办、标记完成、删除待办
  2. 设备显示推送：推送文字到设备、推送图片到设备
  3. 设备管理：获取已绑定的设备列表
  4. 极趣、实验室、设备API、待办、display、推送图片、推送文字
metadata:
  openclaw:
    emoji: "🔬"
---

# 极趣实验室 API 技能

## 快速开始

首次使用前，请在代码中配置你的 API Key 和设备 MAC 地址：

```javascript
const CONFIG = {
  API_KEY: "你的APIKey",      // 在极趣云平台获取
  MAC: "AA:BB:CC:DD:EE:FF"    // 你的设备MAC地址
};
```

## API 配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| Base URL | `https://cloud.zectrix.com/open/v1` | 固定不变 |
| 认证方式 | Header `X-API-Key` | 需要申请 |
| API Key | 用户自行配置 | 在极趣云平台申请 |

## 可用操作
| 功能           | 说明                                      |
| :------------- | :---------------------------------------- |
| `getDevices`   | 获取已绑定的设备列表                      |
| `getTodos`     | 获取待办列表（支持 status/deviceId 过滤） |
| `createTodo`   | 创建待办事项                              |
| `updateTodo`   | 更新待办内容                              |
| `completeTodo` | 标记待办完成                              |
| `deleteTodo`   | 删除待办                                  |
| `pushText`     | 推送文本到设备显示屏                      |
| `pushImage`    | 推送图片到设备显示屏                      |

**使用示例**:

- “查看我的设备有哪些”
- “帮我创建一个待办：买牛奶”
- “在屏幕上显示今日天气：晴”
- “推送桌面上的test.png到设备”


### 1. 获取设备列表

```javascript
// 先获取设备列表，找到你的设备MAC
const devices = await apiCall('getDevices');
// 返回: [{ deviceId: "AA:BB:CC:DD:EE:FF", alias: "我的设备", board: "bread-compact-wifi" }]
```

### 2. 获取待办列表

```javascript
// 获取所有待办
const todos = await apiCall('getTodos');

// 过滤待完成
const pendingTodos = await apiCall('getTodos', { status: 0 });

// 过滤指定设备
const deviceTodos = await apiCall('getTodos', { deviceId: "AA:BB:CC:DD:EE:FF" });
```

### 3. 创建待办 ⚠️ 默认写入设备

```javascript
// 创建的待办会自动关联到配置的MAC设备
const newTodo = await apiCall('createTodo', {
  title: "买牛奶",
  description: "",
  dueDate: "2026-03-20",
  dueTime: "09:00",
  repeatType: "none",  // daily/weekly/monthly/yearly/none
  priority: 1,         // 0=普通, 1=重要, 2=紧急
  // deviceId 自动使用配置的 MAC 地址
});
```

**注意**：创建待办时，默认会自动关联到配置的 MAC 设备，无需手动指定。

### 4. 更新待办

```javascript
const updated = await apiCall('updateTodo', 1, {
  title: "买牛奶和面包",
  description: "新增描述",
  dueDate: "2026-03-21",
  priority: 2
});
```

### 5. 标记完成/取消完成

```javascript
await apiCall('completeTodo', 1);  // 标记完成
await apiCall('uncompleteTodo', 1); // 取消完成
```

### 6. 删除待办

```javascript
await apiCall('deleteTodo', 1);
```

### 7. 推送文本到设备显示屏

```javascript
const result = await apiCall('pushText', 'DC:B4:D9:22:CD:20', {
  text: "今日天气：晴\n温度：25°C",
  fontSize: 20,        // 12-48，默认20
  pageId: "1"          // 1-5，可选，指定会持久化存储
});
// 返回: { totalPages: 1, pushedPages: 1, pageId: "1" }
```

### 8. 推送图片到设备显示屏

```javascript
// 注意：需要使用 FormData 上传图片文件
const formData = new FormData();
formData.append('images', fileInput.files[0]);
formData.append('dither', 'true');
formData.append('pageId', '1');

const result = await apiCall('pushImageForm', 'DC:B4:D9:22:CD:20', formData);
```

## 内部实现

```javascript
const BASE_URL = 'https://cloud.zectrix.com/open/v1';

async function apiCall(endpoint, paramsOrData = {}, method = 'GET') {
  const isGet = method === 'GET';
  const url = new URL(`${BASE_URL}/${endpoint}`);
  
  const options = {
    method,
    headers: {
      'X-API-Key': '你的APIKey'  // 替换为你的API Key
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
```

## 错误处理

所有API返回格式：
```javascript
{ code: 0, data: {...} }  // 成功
{ code: 非0, msg: "错误信息" }  // 失败
```

检查 `code === 0` 确认成功。

## 🔐 安全提示

- **API Key** 是你的个人凭证，请勿泄露到公开场合
- **MAC 地址** 是设备标识，通常可以公开
- 使用完毕后请妥善保管凭证
