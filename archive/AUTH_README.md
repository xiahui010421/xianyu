# Web服务认证配置说明

## 概述

本项目的Web服务现在支持Basic认证，确保只有授权用户才能访问管理界面和API。

## 配置方法

### 1. 环境变量配置

在 `.env` 文件中添加以下配置：

```bash
# Web服务认证配置
WEB_USERNAME=admin
WEB_PASSWORD=admin123
```

### 2. 默认凭据

如果未在 `.env` 文件中设置认证凭据，系统将使用以下默认值：
- 用户名：`admin`
- 密码：`admin123`

**⚠️ 重要：生产环境请务必修改默认密码！**

## 认证范围

### 需要认证的端点

以下所有API端点和页面都需要Basic认证：

- **Web界面**：`/` - 主管理界面
- **任务管理**：
  - `GET /api/tasks` - 获取任务列表
  - `POST /api/tasks/generate` - AI生成任务
  - `POST /api/tasks` - 创建任务
  - `PATCH /api/tasks/{task_id}` - 更新任务
  - `POST /api/tasks/start/{task_id}` - 启动任务
  - `POST /api/tasks/stop/{task_id}` - 停止任务
  - `DELETE /api/tasks/{task_id}` - 删除任务
- **日志管理**：
  - `GET /api/logs` - 获取日志
  - `DELETE /api/logs` - 清空日志
- **结果管理**：
  - `GET /api/results/files` - 获取结果文件列表
  - `GET /api/results/{filename}` - 获取结果文件内容
  - `DELETE /api/results/files/{filename}` - 删除结果文件
- **系统设置**：
  - `GET /api/settings/status` - 获取系统状态
  - `GET /api/settings/notifications` - 获取通知设置
  - `PUT /api/settings/notifications` - 更新通知设置
- **Prompt管理**：
  - `GET /api/prompts` - 获取prompt文件列表
  - `GET /api/prompts/{filename}` - 获取prompt文件内容
  - `PUT /api/prompts/{filename}` - 更新prompt文件
- **登录状态管理**：
  - `POST /api/login-state` - 更新登录状态
  - `DELETE /api/login-state` - 删除登录状态
- **静态文件**：`/static/*` - CSS、JS、图片等静态资源

### 不需要认证的端点

- `GET /health` - 健康检查端点

## 使用方法

### 1. 浏览器访问

当你在浏览器中访问Web界面时，会弹出认证对话框，输入配置的用户名和密码即可。

### 2. API调用

使用API时，需要在请求头中包含Basic认证信息：

```bash
# 使用curl示例
curl -u admin:admin123 http://localhost:8000/api/tasks

# 使用Python requests示例
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'http://localhost:8000/api/tasks',
    auth=HTTPBasicAuth('admin', 'admin123')
)
```

### 3. JavaScript前端

前端JavaScript代码会自动处理认证，无需修改。

## 安全建议

1. **修改默认密码**：生产环境务必修改默认的用户名和密码
2. **使用强密码**：密码应包含大小写字母、数字和特殊字符
3. **HTTPS部署**：生产环境建议使用HTTPS协议
4. **定期更换密码**：建议定期更换认证凭据
5. **限制访问IP**：可以通过防火墙限制访问IP范围

## 故障排除

### 认证失败

1. 检查 `.env` 文件中的 `WEB_USERNAME` 和 `WEB_PASSWORD` 配置
2. 确认环境变量已正确加载
3. 检查用户名和密码是否正确输入

### 静态资源无法加载

1. 确认浏览器已通过认证
2. 检查静态文件路径是否正确
3. 查看浏览器开发者工具的网络请求

## 配置示例

### 完整的 .env 配置示例

```bash
# Web服务认证配置
WEB_USERNAME=myadmin
WEB_PASSWORD=MySecurePassword123!

# 其他配置...
OPENAI_API_KEY=your_openai_api_key
NTFY_TOPIC_URL=https://ntfy.sh/your_topic
```

### Docker部署配置

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - WEB_USERNAME=admin
      - WEB_PASSWORD=secure_password_here
    volumes:
      - ./config.json:/app/config.json
      - ./logs:/app/logs
      - ./results:/app/results
``` 