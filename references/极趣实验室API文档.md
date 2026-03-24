# 极趣实验室 API 文档

## 基础说明

所有接口的基础地址为：`https://cloud.zectrix.com/open/v1`

所有请求都需要在请求头中携带你的 API Key：



```
X-API-Key: 你的API Key
```



***

## 设备管理

### 获取设备列表

获取你账号下绑定的所有设备信息。

**请求信息**



* 请求方法：`GET`

* 请求地址：`/devices`

**返回示例**



```
{

&#x20; "code": 0,

&#x20; "data": \[

&#x20;   {

&#x20;     "deviceId": "AA:BB:CC:DD:EE:FF",

&#x20;     "alias": "我的设备",

&#x20;     "board": "bread-compact-wifi"

&#x20;   }

&#x20; ]

}
```

**curl 示例**



```
curl \\

&#x20; "https://cloud.zectrix.com/open/v1/devices" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da"
```



***

## 待办事项管理

### 获取待办列表

获取待办事项列表，支持过滤状态和设备。

**请求信息**



* 请求方法：`GET`

* 请求地址：`/todos`

**查询参数**



| 参数名      | 类型      | 必填 | 说明                        |
| -------- | ------- | -- | ------------------------- |
| status   | integer | 否  | 过滤状态: 0 = 待完成，1 = 已完成     |
| deviceId | string  | 否  | 设备 ID (MAC 地址), 过滤指定设备的待办 |

**返回示例**



```
{

&#x20; "code": 0,

&#x20; "data": \[

&#x20;   {

&#x20;     "id": 1,

&#x20;     "title": "买牛奶",

&#x20;     "description": "",

&#x20;     "dueDate": "2026-03-20",

&#x20;     "dueTime": "09:00",

&#x20;     "repeatType": "none",

&#x20;     "status": 0,

&#x20;     "priority": 1,

&#x20;     "completed": false,

&#x20;     "deviceId": "AA:BB:CC:DD:EE:FF",

&#x20;     "deviceName": "我的设备",

&#x20;     "createDate": "2026-03-18 10:00:00",

&#x20;     "updateDate": 1742284800

&#x20;   }

&#x20; ]

}
```

**curl 示例**



```
curl \\

&#x20; "https://cloud.zectrix.com/open/v1/todos?status=0\&deviceId=AA:BB:CC:DD:EE:FF" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da"
```



***

### 创建待办

创建一个新的待办事项。

**请求信息**



* 请求方法：`POST`

* 请求地址：`/todos`

**请求体参数**



| 参数名           | 类型      | 必填 | 说明                                     |
| ------------- | ------- | -- | -------------------------------------- |
| title         | string  | 是  | 标题                                     |
| description   | string  | 否  | 描述                                     |
| dueDate       | string  | 否  | 截止日期 (yyyy-MM-dd)                      |
| dueTime       | string  | 否  | 截止时间 (HH:mm)                           |
| repeatType    | string  | 否  | 重复类型: daily/weekly/monthly/yearly/none |
| repeatWeekday | integer | 否  | 周几 0-6, 0 = 周日 (weekly 用)              |
| repeatMonth   | integer | 否  | 每年几月 1-12 (yearly 用)                   |
| repeatDay     | integer | 否  | 每月几号 1-31 (monthly/yearly 用)           |
| priority      | integer | 否  | 优先级: 0 = 普通，1 = 重要，2 = 紧急              |
| deviceId      | string  | 否  | 设备 ID (MAC 地址), 为空则为个人待办               |

**请求体示例**



```
{

&#x20; "title": "买牛奶",

&#x20; "description": "",

&#x20; "dueDate": "2026-03-20",

&#x20; "dueTime": "09:00",

&#x20; "repeatType": "none",

&#x20; "priority": 1,

&#x20; "deviceId": "AA:BB:CC:DD:EE:FF"

}
```

**返回示例**



```
{

&#x20; "code": 0,

&#x20; "data": {

&#x20;   "id": 1,

&#x20;   "title": "买牛奶",

&#x20;   "status": 0,

&#x20;   "priority": 1,

&#x20;   "deviceId": "AA:BB:CC:DD:EE:FF",

&#x20;   "createDate": "2026-03-18 10:00:00"

&#x20; }

}
```

**curl 示例**



```
curl \\

&#x20; -X POST \\

&#x20; "https://cloud.zectrix.com/open/v1/todos" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da" \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"title":"买牛奶","description":"","dueDate":"2026-03-20","dueTime":"09:00","repeatType":"none","priority":1,"deviceId":"AA:BB:CC:DD:EE:FF"}'
```



***

### 更新待办

更新已有的待办事项信息。

**请求信息**



* 请求方法：`PUT`

* 请求地址：`/todos/{id}`

**路径参数**



| 参数名 | 类型      | 必填 | 说明    |
| --- | ------- | -- | ----- |
| id  | integer | 是  | 待办 ID |

**请求体参数**



| 参数名         | 类型      | 必填 | 说明                       |
| ----------- | ------- | -- | ------------------------ |
| title       | string  | 否  | 标题                       |
| description | string  | 否  | 描述                       |
| dueDate     | string  | 否  | 截止日期 (yyyy-MM-dd)        |
| dueTime     | string  | 否  | 截止时间 (HH:mm)             |
| priority    | integer | 否  | 优先级：0 = 普通，1 = 重要，2 = 紧急 |

**请求体示例**



```
{

&#x20; "title": "买牛奶和面包"

}
```

**返回示例**



```
{

&#x20; "code": 0,

&#x20; "data": {

&#x20;   "id": 1,

&#x20;   "title": "买牛奶和面包",

&#x20;   "status": 0,

&#x20;   "priority": 1

&#x20; }

}
```

**curl 示例**



```
curl \\

&#x20; -X PUT \\

&#x20; "https://cloud.zectrix.com/open/v1/todos/1" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da" \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"title":"买牛奶和面包"}'
```



***

### 标记待办完成 / 取消完成

切换待办的完成状态，已完成的会变成未完成，未完成的会变成已完成。

**请求信息**



* 请求方法：`PUT`

* 请求地址：`/todos/{id}/complete`

**路径参数**



| 参数名 | 类型      | 必填 | 说明    |
| --- | ------- | -- | ----- |
| id  | integer | 是  | 待办 ID |

**返回示例**



```
{ "code": 0, "msg": "success" }
```

**curl 示例**



```
curl \\

&#x20; -X PUT \\

&#x20; "https://cloud.zectrix.com/open/v1/todos/1/complete" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da"
```



***

### 删除待办

删除指定的待办事项。

**请求信息**



* 请求方法：`DELETE`

* 请求地址：`/todos/{id}`

**路径参数**



| 参数名 | 类型      | 必填 | 说明    |
| --- | ------- | -- | ----- |
| id  | integer | 是  | 待办 ID |

**返回示例**



```
{ "code": 0, "msg": "success" }
```

**curl 示例**



```
curl \\

&#x20; -X DELETE \\

&#x20; "https://cloud.zectrix.com/open/v1/todos/1" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da"
```



***

## 设备内容推送

### 推送图片到设备

将本地图片推送到设备的墨水屏显示。

**请求信息**



* 请求方法：`POST`

* 请求地址：`/devices/{deviceId}/display/image`

**路径参数**



| 参数名      | 类型     | 必填 | 说明             |
| -------- | ------ | -- | -------------- |
| deviceId | string | 是  | 设备 ID (MAC 地址) |

**表单参数**



| 参数名    | 类型      | 必填 | 说明                             |
| ------ | ------- | -- | ------------------------------ |
| images | file    | 是  | 图片文件，支持多张 (最多 5 张)，单张不超过 2MB   |
| dither | boolean | 否  | 是否使用抖动算法 (默认 true)，关闭则使用硬阈值二值化 |
| pageId | string  | 否  | 页面编号 (1-5)，指定后会持久化存储到设备        |

**返回示例**



```
{

&#x20; "code": 0,

&#x20; "data": {

&#x20;   "totalPages": 1,

&#x20;   "pushedPages": 1,

&#x20;   "pageId": "1"

&#x20; }

}
```

**curl 示例**



```
curl \\

&#x20; -X POST \\

&#x20; "https://cloud.zectrix.com/open/v1/devices/DC:B4:D9:22:CD:20/display/image" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da" \\

&#x20; -F "images=@/path/to/image.png" \\

&#x20; -F "dither=true" \\

&#x20; -F "pageId=1"
```



***

### 推送文本到设备

将文本内容推送到设备的墨水屏显示。

**请求信息**



* 请求方法：`POST`

* 请求地址：`/devices/{deviceId}/display/text`

**路径参数**



| 参数名      | 类型     | 必填 | 说明             |
| -------- | ------ | -- | -------------- |
| deviceId | string | 是  | 设备 ID (MAC 地址) |

**请求体参数**



| 参数名      | 类型      | 必填 | 说明                      |
| -------- | ------- | -- | ----------------------- |
| text     | string  | 是  | 文本内容 (最多 5000 字)，支持换行   |
| fontSize | integer | 否  | 字体大小 (12-48，默认 20)      |
| pageId   | string  | 否  | 页面编号 (1-5)，指定后会持久化存储到设备 |

**请求体示例**



```
{

&#x20; "text": "今日天气：晴\n温度：25°C",

&#x20; "fontSize": 20,

&#x20; "pageId": "1"

}
```

**返回示例**



```
{

&#x20; "code": 0,

&#x20; "data": {

&#x20;   "totalPages": 1,

&#x20;   "pushedPages": 1,

&#x20;   "pageId": "1"

&#x20; }

}
```

**curl 示例**



```
curl \\

&#x20; -X POST \\

&#x20; "https://cloud.zectrix.com/open/v1/devices/DC:B4:D9:22:CD:20/display/text" \\

&#x20; -H "X-API-Key: zt\_f0c3636cf57c6ab4689e6f32801585da" \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"text":"今日天气：晴\n温度：25°C","fontSize":20,"pageId":"1"}'
```

> （注：文档部分内容可能由 AI 生成）