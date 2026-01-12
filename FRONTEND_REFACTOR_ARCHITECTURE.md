# Vue 3 前端重构架构方案 (v1.1)

## 0. 背景与原则

本文档旨在为 `ai-goofish-monitor` 项目的前端重构提供一套完整的工程架构方案。此方案基于对现有后端（FastAPI）和前端（原生 JavaScript）代码的深入分析，并严格遵循以下核心原则：

1.  **复杂度对等**: 确保前端架构的复杂度与后端服务的简洁性相匹配，避免过度设计。
2.  **可维护性优先**: 产出易于理解、易于接手、易于扩展的代码。
3.  **业务驱动**: 任何引入的复杂度（如 WebSocket、RBAC）都必须有明确的业务或未来功能需求支撑。

---

## 1. 模块拆分结构 (Logical Modules)

应用将按功能领域进行逻辑拆分，每个模块都包含其独立的视图、路由、状态逻辑和组件。

-   **`Auth` (认证模块)**
-   **`Tasks` (任务管理模块)**
-   **`Results` (结果查看模块)**
-   **`Logs` (日志模块)**
-   **`Settings` (系统设置模块)**
-   **`Dashboard` (仪表盘模块)** - *为未来预留*
-   **`Core` (核心/共享模块)**

---

## 2. 页面路由树 (Vue Router)

路由设计将遵循模块化，并为未来的权限控制预留 `meta` 字段。

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/tasks',
    children: [
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/TasksView.vue'),
        meta: { title: '任务管理', requiresAuth: true },
      },
      // ... 其他子路由
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', redirect: '/' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ... 路由守卫
export default router;
```

---

## 3. 状态管理设计 (Composables)

采用基于 Vue 3 Composition API 的 **Composable** 函数进行状态管理，放弃引入 Pinia，以降低复杂度。

-   **`useWebSocket.ts`**: 唯一且核心的 WebSocket 管理器，封装连接、重连及消息分发。
-   **`useAuth.ts`**: 管理当前用户的状态和权限，为 RBAC 提供基础。
-   **`useTasks.ts`**: 封装 `Tasks` 模块的所有业务逻辑，并响应 WebSocket 推送。
-   **`useLogs.ts`**: 封装 `Logs` 模块的业务逻辑，并响应 WebSocket 推送。

---

## 4. UI 构建方案 (UI Implementation Strategy)

我们将采用 **`shadcn-vue`** 作为 UI 的构建方案。

-   **核心理念**: `shadcn-vue` **不是一个组件库**，而是一系列可复用组件的**代码集合**。我们通过其 CLI 将组件源代码直接复制到项目中。
-   **技术栈**:
    -   **样式**: **Tailwind CSS**。所有组件都基于其原子化类名构建，提供最大化的样式控制力。
    -   **底层**: **Radix Vue**。提供无头（headless）、功能完备且高度符合 WAI-ARIA 标准的底层组件原语。
-   **Implications**:
    -   **组件所有权**: 我们 100% 拥有组件代码，可以随意修改以满足设计需求，无需覆盖库的样式。
    -   **可维护性**: 由于代码在本地，追踪和调试组件行为变得非常直接。
    -   **打包体积**: 最终产物只包含实际使用的代码和样式，体积更小。
    -   **开发流程**: 初始设置（如配置 Tailwind）会比使用传统组件库稍复杂，但后续开发和定制会更高效。

---

## 5. 接口对齐表 (API Alignment)

| 模块 | 功能 | HTTP 方法 | API Endpoint | Vue 调用函数 |
| :--- | :--- | :--- | :--- | :--- |
| **Tasks** | 获取所有任务 | `GET` | `/api/tasks` | `api.tasks.getAll()` |
| | AI 创建任务 | `POST` | `/api/tasks/generate` | `api.tasks.createWithAI()` |
| | ... | ... | ... | ... |
| **Results** | 获取结果文件列表 | `GET` | `/api/results/files` | `api.results.getFiles()` |
| | ... | ... | ... | ... |
| **Logs** | 获取日志 | `GET` | `/api/logs` | `api.logs.get()` |
| | ... | ... | ... | ... |
| **Settings**| 获取系统状态 | `GET` | `/api/settings/status` | `api.settings.getStatus()` |
| | ... | ... | ... | ... |

*(表格内容与 v1.0 版本一致)*

---

## 6. 目录结构

新的 `web-ui` 目录将采用功能驱动和分层结合的结构。

```
web-ui/
├── src/
│   ├── api/             # API 请求层
│   ├── assets/          # 静态资源
│   ├── components/      # 全局及 shadcn-vue 生成的组件
│   │   ├── ui/          #   - shadcn-vue 生成的 UI 组件 (e.g., button.vue, dialog.vue)
│   │   └── common/      #   - 项目自身的通用业务组件
│   ├── composables/     # 状态与业务逻辑
│   ├── layouts/         # 页面主布局
│   ├── router/          # 路由配置
│   ├── services/        # 核心服务 (e.g., websocket.ts)
│   ├── lib/             # Tailwind CSS 相关工具 (e.g., utils.ts)
│   ├── types/           # TypeScript 类型定义
│   └── views/           # 页面级视图组件
├── tailwind.config.js   # Tailwind CSS 配置文件
├── components.json      # shadcn-vue 配置文件
├── vite.config.ts
└── package.json
```

---

## 7. 组件设计边界

组件将严格划分为“容器组件”和“展示组件”。

-   **`TasksView.vue` (容器/视图组件)**
    -   **职责**: 页面入口，调用 `useTasks()` 获取数据和方法，传递给子组件。
    -   **内部**: `const { tasks, isLoading, createTask } = useTasks();`

-   **`TasksTable.vue` (展示组件)**
    -   **职责**: 接收任务列表并使用 `shadcn-vue` 的 `Table` 组件进行渲染。当用户操作时，**只发出事件**。
    -   **Props**: `tasks: Task[]`, `isLoading: boolean`。
    -   **Emits**: `@edit-task`, `@delete-task`, `@run-task`, `@stop-task`。

-   **`TaskFormWizard.vue` (容器/功能组件)**
    -   **职责**: 实现任务创建的多步引导流程，使用 `shadcn-vue` 的 `Dialog`, `Input`, `Button` 等组件构建。
    -   **Props**: `initialData?: Task`。
    -   **Emits**: `@save`。

---

## 8. 渲染层与业务层的解耦说明

核心思想是**清晰地分离渲染、业务逻辑和数据请求**。

1.  **渲染层 (Views & Components)**:
    -   **角色**: “哑”组件。只负责“看什么样”。
    -   **实现**: 使用 Vue 模板语法、**由 `shadcn-vue` 生成并由我们维护的 UI 组件**以及 **Tailwind CSS** 类名。接收 `props` 数据进行渲染，通过 `emits` 报告用户交互。

2.  **业务逻辑层 (Composables)**:
    -   **角色**: “聪明”的协调者。负责“做什么”。
    -   **实现**: `use...` 函数。它们是响应式的、有状态的逻辑单元，负责调用 API、处理数据，并暴露给渲染层。

3.  **数据服务层 (API & Services)**:
    -   **角色**: 数据的“搬运工”。负责“从哪拿数据”。
    -   **实现**: 在 `src/api` 目录下类型化的 API 请求函数，以及 `src/services` 下的 WebSocket 服务。

#### 数据流示例 (单向数据流):

`用户点击“删除”按钮` -> `TaskTableRow.vue` **emits** `@delete` 事件 -> `TasksView.vue` 监听到事件，调用 `useTasks()` 提供的 `deleteTask(id)` 方法 -> `useTasks.ts` 调用 `api.tasks.delete(id)` -> `api/tasks.ts` 发出 `fetch` 请求 -> 成功后 `useTasks.ts` 更新内部的 `tasks` ref -> `TasksView.vue` 自动响应 `tasks` 的变化并重新渲染 `TasksTable.vue`。