import requests
from typing import Optional, Dict, Any, List

# ==================== 配置项 - 请根据你的个人信息修改这里 ====================
API_KEY = "zt_f0c3636cf57c6ab4689e6f32801585da"
DEVICE_MAC = "DC:B4:D9:22:CD:20"
# ======================================================================

# 基础API地址
BASE_URL = "https://cloud.zectrix.com/open/v1"

def _get_headers() -> Dict[str, str]:
    """获取请求头"""
    return {
        "X-API-Key": API_KEY
    }

def _handle_response(response: requests.Response) -> Dict[str, Any]:
    """处理API响应，处理错误"""
    response.raise_for_status()
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"API调用失败: {result.get('msg', '未知错误')}")
    return result

def get_devices() -> List[Dict[str, Any]]:
    """
    获取设备列表
    返回: 设备信息列表，包含deviceId(MAC地址)、别名、设备型号
    """
    url = f"{BASE_URL}/devices"
    response = requests.get(url, headers=_get_headers())
    result = _handle_response(response)
    return result.get("data", [])

def get_todos(status: Optional[int] = None, device_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    获取待办事项列表
    参数:
        status: 过滤状态，0=待完成，1=已完成，不传则返回所有
        device_id: 设备ID(MAC地址)，过滤指定设备的待办：
            - 不传：默认获取配置的默认设备的待办
            - 传非空值：获取指定设备的待办
            - 传空字符串：获取所有待办（包括个人待办）
    返回: 待办事项列表
    """
    url = f"{BASE_URL}/todos"
    params = {}
    if status is not None:
        params["status"] = status
    
    # 处理device_id参数
    if device_id is None:
        # 用户未传参，默认使用配置的设备
        params["deviceId"] = DEVICE_MAC
    elif device_id:
        # 用户传了非空值，使用指定的设备
        params["deviceId"] = device_id
    # 用户传了空字符串，不添加deviceId参数，获取所有待办
    
    response = requests.get(url, headers=_get_headers(), params=params)
    result = _handle_response(response)
    return result.get("data", [])

def create_todo(
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    repeat_type: str = "none",
    priority: int = 0,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    创建待办事项
    参数:
        title: 待办标题（必填）
        description: 待办描述
        due_date: 截止日期，格式yyyy-MM-dd
        due_time: 截止时间，格式HH:mm
        repeat_type: 重复类型，可选daily/weekly/monthly/yearly/none，默认none
        priority: 优先级，0=普通,1=重要,2=紧急，默认0
        device_id: 绑定的设备ID(MAC地址)：
            - 不传：默认绑定到配置的默认设备
            - 传非空值：绑定到指定的设备
            - 传空字符串：不绑定，创建个人待办
    返回: 创建成功的待办信息
    """
    url = f"{BASE_URL}/todos"
    data: Dict[str, Any] = {
        "title": title,
        "repeatType": repeat_type,
        "priority": priority
    }
    if description is not None:
        data["description"] = description
    if due_date is not None:
        data["dueDate"] = due_date
    if due_time is not None:
        data["dueTime"] = due_time
    
    # 处理device_id参数
    if device_id is None:
        # 用户未传参，默认绑定到配置的设备
        data["deviceId"] = DEVICE_MAC
    elif device_id:
        # 用户传了非空值，绑定到指定的设备
        data["deviceId"] = device_id
    # 用户传了空字符串，不添加deviceId参数，创建个人待办
    
    headers = _get_headers()
    headers["Content-Type"] = "application/json"
    response = requests.post(url, headers=headers, json=data)
    result = _handle_response(response)
    return result.get("data", {})

def update_todo(todo_id: int, **kwargs) -> Dict[str, Any]:
    """
    更新待办事项
    参数:
        todo_id: 待办ID（必填）
        **kwargs: 要更新的字段，支持title/description/dueDate/dueTime/priority等
    示例:
        update_todo(1, title="新标题", priority=2)
    返回: 更新后的待办信息
    """
    url = f"{BASE_URL}/todos/{todo_id}"
    headers = _get_headers()
    headers["Content-Type"] = "application/json"
    response = requests.put(url, headers=headers, json=kwargs)
    result = _handle_response(response)
    return result.get("data", {})

def complete_todo(todo_id: int) -> str:
    """
    标记待办事项为完成/取消完成（切换状态）
    参数:
        todo_id: 待办ID
    返回: 操作结果信息
    """
    url = f"{BASE_URL}/todos/{todo_id}/complete"
    response = requests.put(url, headers=_get_headers())
    _handle_response(response)
    return "操作成功"

def delete_todo(todo_id: int) -> str:
    """
    删除待办事项
    参数:
        todo_id: 待办ID
    返回: 操作结果信息
    """
    url = f"{BASE_URL}/todos/{todo_id}"
    response = requests.delete(url, headers=_get_headers())
    _handle_response(response)
    return "删除成功"

def push_text(
    text: str,
    font_size: int = 20,
    page_id: Optional[str] = None,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    推送文本内容到设备墨水屏
    参数:
        text: 文本内容，最多5000字，支持换行
        font_size: 字体大小，12-48，默认20
        page_id: 页面编号(1-5)，指定后会持久化存储到设备
        device_id: 设备ID(MAC地址)，不传则使用配置中的默认设备
    返回: 推送结果
    """
    device_id = device_id or DEVICE_MAC
    url = f"{BASE_URL}/devices/{device_id}/display/text"
    
    data: Dict[str, Any] = {
        "text": text,
        "fontSize": font_size
    }
    if page_id is not None:
        data["pageId"] = page_id
    
    headers = _get_headers()
    headers["Content-Type"] = "application/json"
    response = requests.post(url, headers=headers, json=data)
    result = _handle_response(response)
    return result.get("data", {})

def push_image(
    image_path: str,
    dither: bool = True,
    page_id: Optional[str] = None,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    推送图片到设备墨水屏
    参数:
        image_path: 本地图片文件路径，单张不超过2MB
        dither: 是否使用抖动算法，默认True，关闭则使用硬阈值二值化
        page_id: 页面编号(1-5)，指定后会持久化存储到设备
        device_id: 设备ID(MAC地址)，不传则使用配置中的默认设备
    返回: 推送结果
    """
    device_id = device_id or DEVICE_MAC
    url = f"{BASE_URL}/devices/{device_id}/display/image"
    
    files = {
        "images": open(image_path, "rb")
    }
    data = {
        "dither": str(dither).lower()
    }
    if page_id is not None:
        data["pageId"] = page_id
    
    response = requests.post(url, headers=_get_headers(), files=files, data=data)
    # 关闭文件
    files["images"].close()
    result = _handle_response(response)
    return result.get("data", {})
