# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 Playwright 和 AI 的闲鱼智能监控机器人，提供完整的 Web 管理界面。系统采用 FastAPI 后端 + Vue 3 前端架构，支持多任务并发监控、AI 驱动的商品分析和多渠道通知推送。

## 核心架构

### 后端架构（已完成重构）

项目采用清晰的分层架构：

```
API层 (src/api/routes)
    ↓
服务层 (src/services)
    ↓
领域层 (src/domain)
    ↓
基础设施层 (src/infrastructure)
```

**关键组件：**

- **主应用入口**: `src/app.py` - FastAPI 应用，整合所有路由和服务
- **爬虫核心**: `src/scraper.py` - Playwright 驱动的闲鱼爬虫逻辑
- **任务执行器**: `spider_v2.py` - 命令行入口，支持单任务和多任务执行
- **领域模型**: `src/domain/models/task.py` - Task 实体和 DTOs
- **服务层**:
  - `TaskService` - 任务管理
  - `ProcessService` - 进程管理（启动/停止爬虫）
  - `SchedulerService` - 定时调度（基于 APScheduler）
  - `AIAnalysisService` - AI 分析服务
  - `NotificationService` - 通知服务（支持 ntfy、Bark、企业微信、Telegram、Webhook）
- **仓储层**: `JsonTaskRepository` - 基于 JSON 文件的任务持久化

### 前端架构（Vue 3 重构中）

位于 `web-ui/` 目录，采用 Vue 3 + TypeScript + Vite + shadcn-vue + Tailwind CSS：

```
web-ui/
├── src/
│   ├── api/             # API 请求层
│   ├── components/      # 全局组件和 shadcn-vue UI 组件
│   ├── composables/     # 状态与业务逻辑
│   ├── layouts/         # 页面主布局
│   ├── router/          # 路由配置
│   ├── services/        # 核心服务（如 WebSocket）
│   ├── types/           # TypeScript 类型定义
│   └── views/           # 页面级视图组件
```

**设计原则**：
- 渲染层与业务层解耦
- 容器组件（智能）vs 展示组件（哑）
- Composables 管理状态和业务逻辑

## 开发环境设置

### 后端开发

```bash
# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，至少配置：
# - OPENAI_API_KEY
# - OPENAI_BASE_URL
# - OPENAI_MODEL_NAME

# 启动开发服务器
python -m src.app
# 或使用 uvicorn
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### 前端开发

```bash
cd web-ui

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### Docker 部署

```bash
# 启动服务
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 常用命令

### 运行爬虫任务

```bash
# 运行所有启用的任务
python spider_v2.py

# 运行指定任务
python spider_v2.py --task-name "MacBook Air M1"

# 调试模式（限制处理商品数量）
python spider_v2.py --debug-limit 3

# 使用自定义配置文件
python spider_v2.py --config custom_config.json
```

### 测试

```bash
# 运行后端测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src

# 测试新架构 API
python test_new_api.py
```

## 配置文件说明

### config.json

任务配置文件，定义所有监控任务：

```json
{
  "task_name": "任务名称",
  "enabled": true,
  "keyword": "搜索关键词",
  "description": "任务描述",
  "max_pages": 5,
  "personal_only": true,
  "min_price": "3000",
  "max_price": "5000",
  "cron": "0 */2 * * *",
  "ai_prompt_base_file": "prompts/base_prompt.txt",
  "ai_prompt_criteria_file": "prompts/macbook_criteria.txt",
  "is_running": false
}
```

### .env

环境变量配置，关键配置项：

- **AI 模型**: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL_NAME`
- **通知服务**: `NTFY_TOPIC_URL`, `BARK_URL`, `WX_BOT_URL`, `TELEGRAM_BOT_TOKEN`
- **爬虫设置**: `RUN_HEADLESS`, `LOGIN_IS_EDGE`
- **Web 认证**: `WEB_USERNAME`, `WEB_PASSWORD`
- **服务端口**: `SERVER_PORT`

## 数据流程

1. **任务创建** → Web UI 或直接编辑 `config.json`
2. **任务调度** → `SchedulerService` 根据 cron 表达式或手动触发
3. **进程启动** → `ProcessService` 启动 `spider_v2.py` 子进程
4. **商品爬取** → `scraper.py` 使用 Playwright 抓取闲鱼商品
5. **AI 分析** → `AIAnalysisService` 调用多模态模型分析商品图片和描述
6. **通知推送** → `NotificationService` 根据 AI 推荐结果发送通知
7. **数据存储** → 结果保存到 `jsonl/` 目录，图片保存到 `images/`

## 关键技术点

### 登录状态管理

- 登录状态存储在 `state.json` 文件中
- 通过 Chrome 扩展提取登录信息（无法在 Docker 内扫码登录）
- Web UI 提供"手动更新登录状态"功能

### 进程管理

- `ProcessService` 使用 `asyncio.create_subprocess_exec` 管理爬虫进程
- 每个任务运行在独立的子进程中
- 支持进程组管理（Unix）和优雅终止

### 定时调度

- 基于 APScheduler 的 `BackgroundScheduler`
- 支持 Cron 表达式配置
- 应用启动时自动加载所有定时任务

### AI 分析

- 支持多模态模型（需支持图片上传）
- 使用两阶段 Prompt：base_prompt + criteria_prompt
- 返回结构化 JSON 结果（推荐/不推荐 + 理由）

### 通知系统

插件化设计，支持多种通知渠道：
- ntfy.sh
- Bark
- 企业微信 Webhook
- Telegram Bot
- Gotify
- 通用 Webhook

## API 端点

主要 API 路由（需 Basic Auth）：

- `GET /` - Web UI 主页
- `GET /health` - 健康检查（无需认证）
- `GET /api/tasks` - 获取所有任务
- `POST /api/tasks` - 创建任务
- `PUT /api/tasks/{task_id}` - 更新任务
- `DELETE /api/tasks/{task_id}` - 删除任务
- `POST /api/tasks/{task_id}/start` - 启动任务
- `POST /api/tasks/{task_id}/stop` - 停止任务
- `GET /api/logs` - 获取日志
- `GET /api/results` - 获取监控结果
- `GET /api/settings/check` - 检查系统配置
- `GET /api/prompts` - 获取 Prompt 文件列表
- `GET /api/login-state` - 获取登录状态

完整 API 文档：启动服务后访问 `http://localhost:8000/docs`

## 文件结构关键路径

- `src/app.py` - FastAPI 应用主入口
- `src/scraper.py` - 爬虫核心逻辑
- `spider_v2.py` - 命令行任务执行器
- `src/services/` - 所有业务服务
- `src/api/routes/` - API 路由定义
- `src/domain/models/` - 领域模型
- `src/infrastructure/` - 基础设施（配置、持久化、外部客户端）
- `config.json` - 任务配置
- `state.json` - 登录状态
- `prompts/` - AI Prompt 模板
- `jsonl/` - 监控结果数据
- `logs/` - 日志文件
- `images/` - 下载的商品图片

## 注意事项

1. **登录状态**: Docker 部署时必须通过 Web UI 手动更新登录状态
2. **浏览器依赖**: 需要安装 Playwright 浏览器驱动
3. **AI 模型**: 必须使用支持多模态（图片）的模型
4. **反爬虫**: 避免过于频繁的请求，遇到滑动验证码时可设置 `RUN_HEADLESS=false` 手动处理
5. **认证**: 生产环境务必修改默认的 Web 认证密码
6. **端口冲突**: 默认端口 8000，可通过 `SERVER_PORT` 环境变量修改

## 参考文档

- 重构完成报告: `archive/REFACTORING_COMPLETE.md`
- 前端架构方案: `FRONTEND_REFACTOR_ARCHITECTURE.md`
- 常见问题: `FAQ.md`
- 免责声明: `DISCLAIMER.md`
