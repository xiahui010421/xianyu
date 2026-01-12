# 本地运行指南 

## 🐳 Docker 一键启动 (推荐)

只需要 **git clone** 后执行一条命令即可启动：

```bash
git clone <your-repo-url>
cd ai-goofish-monitor
cp .env.example .env
cp config.json.example config.json
docker compose up -d
```

- 访问地址：`http://127.0.0.1:8000`
- 默认账号/密码同下方说明

### 开发模式 (可选)

如果你要开发前端或后端代码，使用开发版 compose：

```bash
docker compose -f docker-compose.dev.yaml up -d --build
```

## 🛠️ 手动安装步骤 

### 第一步：环境准备 (后端 Python)

1.  **克隆项目并进入目录**：
    ```bash
    git clone <your-repo-url>
    cd ai-goofish-monitor
    ```

2.  **创建并激活虚拟环境** (推荐)：
    - **Linux/macOS**:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```
    - **Windows**:
      ```bash
      python -m venv .venv
      .venv\Scripts\activate
      ```

3.  **安装 Python 依赖**：
    ```bash
    pip install -r requirements.txt
    ```

4.  **浏览器准备**：
    本项目在本地运行时默认通过 `channel="chrome"` 调用您系统中已安装的 **Google Chrome** 或 **Microsoft Edge**。
    
    - 请确保您的电脑已安装其中之一。
    - **无需** 运行 `playwright install` 下载额外的浏览器内核。

### 第二步：编译前端 (Vue3 + Shadcn UI)

项目采用前后端分离架构，需要先将前端代码编译打包，后端才能正常提供 Web 界面。

1.  **进入前端目录**：
    
    ```bash
    cd web-ui
    ```
    
2.  **安装 Node.js 依赖**：
    ```bash
    npm install
    ```

3.  **执行构建打包**：
    
    ```bash
    npm run build
    ```
    
4.  **将构建产物移动到后端可访问位置**：
    - **Linux/macOS**:
      ```bash
      rm -rf ../dist && mv dist ../
      ```
    - **Windows (PowerShell)**:
      ```powershell
      Remove-Item -Recurse -Force ..\dist; Move-Item dist ..\
      ```

5.  **返回根目录**：
    ```bash
    cd ..
    ```

### 第三步：配置文件

1.  **创建 `.env` 文件**：
    ```bash
    cp .env.example .env
    ```
    编辑 `.env` 文件，至少填入 `OPENAI_API_KEY`。如果您没有特定的模型需求，建议保持 `OPENAI_BASE_URL` 为默认或使用您可靠的代理地址。

2.  **创建 `config.json` 文件** (任务配置)：
    
    ```bash
    cp config.json.example config.json
    ```

### 第四步：启动服务

在项目根目录下，且确保虚拟环境已激活的状态下运行：

```bash
python web_server.py
```

- **默认地址**：`http://127.0.0.1:8000`
- **默认账号**：`admin`
- **默认密码**：`admin123` (可在 `.env` 中通过 `WEB_USERNAME` 和 `WEB_PASSWORD` 修改)

## 
