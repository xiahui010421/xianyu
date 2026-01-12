# 旧模块归档说明

归档日期：2025-12-31

## 归档原因

这些文件是旧架构的遗留代码，已被新的分层架构替代。为保持代码库整洁，将其归档到此目录。

## 归档文件清单

### 1. task.py
- **原路径**: `src/task.py`
- **功能**: 旧的任务管理模块
- **替代方案**:
  - 领域模型：`src/domain/models/task.py`
  - 服务层：`src/services/task_service.py`
  - 仓储层：`src/infrastructure/persistence/json_task_repository.py`
- **归档原因**: 新架构采用 DDD 分层设计，任务管理逻辑已重构

### 2. file_operator.py
- **原路径**: `src/file_operator.py`
- **功能**: 旧的文件操作工具类
- **替代方案**:
  - 新架构的仓储层直接使用 `aiofiles` 和标准库
  - `JsonTaskRepository` 实现了更专业的持久化逻辑
- **归档原因**: 简化依赖，使用更标准的文件操作方式

### 3. prompt_generator.py
- **原路径**: `prompt_generator.py`
- **功能**: 命令行 Prompt 生成工具
- **替代方案**:
  - Web UI 的任务生成功能（`/api/tasks/generate`）
  - `src/api/routes/settings.py` 中的 AI 生成接口
- **归档原因**: 功能已集成到 Web UI，提供更好的用户体验

## 注意事项

1. 这些文件仅作归档保留，不应在新代码中引用
2. 如需恢复某个功能，请参考新架构的实现方式
3. 测试文件中如有引用这些模块，需要相应更新
