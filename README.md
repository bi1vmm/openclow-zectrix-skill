# 极趣实验室 OpenClaw 技能

一个为极趣实验室智能墨水屏设备打造的 OpenClaw 技能，封装了官方全部 API，默认自动绑定你的个人设备，开箱即用，无需额外配置即可管理待办、推送内容到设备。
非官方开发，仅供测试学习使用

## 功能特性

- 📱 **设备管理**：一键查看你账号下的所有绑定设备
- ✅ **待办事项管理**：待办的增删改查、标记完成，默认自动绑定到你的设备
- 🖼️ **内容推送**：支持向墨水屏设备推送文本、图片内容
- 🔧 **可配置化**：仅需修改两个配置项即可适配任意用户的账号，无需改动业务代码
- 📖 **清晰的文档**：附带排版好的 API 文档，方便开发调试

## 快速开始

### 1. 安装技能

下载本项目的压缩包，解压到你的 OpenClaw 技能目录中。

### 2. 配置个人信息

打开 `scripts/main.py`，修改顶部的配置项，替换成你自己的信息：

```python
# ==================== 配置项 - 请根据你的个人信息修改这里 ====================
API_KEY = "你的API Key"
DEVICE_MAC = "你的设备MAC地址"
# ======================================================================
```

这两个信息可以在极趣实验室的个人中心获取。

### 3. 安装依赖

本技能依赖 `requests` 库来发送 API 请求，如果你还没有安装，执行：

```bash
pip install requests
```

## 使用示例

### 待办事项

```python
# 获取你设备的待完成待办
todos = get_todos(status=0)

# 创建一个新的待办，自动绑定到你的设备
todo = create_todo(
    title="买牛奶",
    description="买常温纯牛奶",
    due_date="2026-03-25",
    priority=1
)

# 标记待办完成
complete_todo(todo['id'])
```

### 内容推送

```python
# 推送天气信息到设备
push_text(
    text="今日天气：晴\n温度：25°C\n空气质量：优",
    font_size=24
)

# 推送图片到设备
push_image("/path/to/your/image.png")
```

## 项目结构

```
jiqu_lab_skill/
├── README.md              # 本说明文件
├── SKILL.md               # OpenClaw 技能定义文件
├── scripts/
│   └── main.py            # 业务脚本，包含所有API封装
├── references/
│   └── 极趣实验室API文档.md    # Markdown版API文档
```

## 参考文档

完整的 API 文档可以参考极趣实验室官方文档https://cloud.zectrix.com/home/api-docs
或查看`references/极趣实验室API文档.md`。

## 作者

**BI1VMM**

- 个人网站：[https://bi1vmm.cn](https://bi1vmm.cn)

## 许可证

MIT
