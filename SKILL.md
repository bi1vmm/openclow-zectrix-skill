---
name: 极趣实验室设备管理技能
version: 1.0.1
description: 用于管理极趣实验室的智能墨水屏设备，支持待办事项管理、文本/图片推送至设备，默认自动绑定到你配置的设备，只需修改配置项即可适配个人账号，开箱即用。
author: OpenClaw Community
tags: [极趣实验室, 设备管理, 待办, 墨水屏, 智能硬件]
---

# 极趣实验室设备管理技能

这个技能可以帮你轻松管理极趣实验室的智能设备，支持待办事项的增删改查，以及向墨水屏设备推送文本、图片内容，默认会自动将待办绑定到你配置的设备上，所有功能都封装好了，你只需要修改两个配置项就可以直接使用。

## 快速开始

### 1. 配置你的个人信息
打开 `scripts/main.py`，修改最顶部的两个配置项：
```python
# ==================== 配置项 - 请根据你的个人信息修改这里 ====================
API_KEY = "你的API Key"
DEVICE_MAC = "你的设备MAC地址"
# ======================================================================
```
这两个信息你可以在极趣实验室的个人中心获取，替换成你自己的就可以了，之后默认的待办操作都会自动使用这个设备。

### 2. 安装依赖
这个技能需要用到 `requests` 库来发送API请求，如果你还没有安装，执行以下命令：
```bash
pip install requests
```

## 功能说明

### 设备管理
#### 获取你的设备列表
查看你账号下绑定的所有设备信息：
```python
devices = get_devices()
print(devices)
```

### 待办事项管理
#### 获取待办列表
默认会获取你配置的默认设备的待办，也可以过滤状态或者指定其他设备：
```python
# 获取默认设备的所有待完成的待办
todos = get_todos(status=0)
# 获取其他指定设备的待办
todos = get_todos(device_id="其他设备的MAC")
# 获取所有设备的所有待办（包括个人待办）
todos = get_todos(device_id="")
```

#### 创建待办
创建一个新的待办事项，默认会自动绑定到你配置的默认设备，也可以手动指定其他设备：
```python
todo = create_todo(
    title="买牛奶",
    description="买常温纯牛奶",
    due_date="2026-03-25",
    due_time="09:00",
    priority=1
)
print(f"创建成功，待办ID: {todo['id']}")

# 如果你想要创建个人待办（不绑定到设备），可以传空的device_id
todo = create_todo(title="个人待办", device_id="")
```

#### 更新待办
修改已有的待办信息：
```python
# 修改待办的标题和优先级
updated_todo = update_todo(todo_id=1, title="买牛奶和面包", priority=2)
```

#### 标记待办完成
切换待办的完成状态：
```python
complete_todo(todo_id=1)
```

#### 删除待办
删除不需要的待办：
```python
delete_todo(todo_id=1)
```

### 设备内容推送
#### 推送文本到设备
把文本内容推送到墨水屏设备，默认推送到你配置的默认设备：
```python
result = push_text(
    text="今日天气：晴\n温度：25°C\n空气质量：优",
    font_size=24
)
print(f"推送成功，共推送了{result['pushedPages']}页")
```

#### 推送图片到设备
把本地图片推送到墨水屏设备，默认推送到你配置的默认设备：
```python
result = push_image(
    image_path="/home/user/photos/my_image.png",
    dither=True
)
print(f"图片推送成功")
```

## 注意事项
1. 推送图片时，单张图片不能超过2MB，最多可以一次推送5张
2. 文本内容最多支持5000字
3. 如果你有多个设备，可以在调用函数的时候传入device_id参数来指定操作的设备
4. 如果需要操作个人待办或者获取所有待办，只需要传入空字符串作为device_id即可

## 参考资料
完整的API文档可以参考极趣实验室官方文档https://cloud.zectrix.com/home/api-docs

或者查看`references/极趣实验室API文档.md`
