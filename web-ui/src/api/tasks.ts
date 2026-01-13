import type { Task, TaskGenerateRequest, TaskUpdate } from '@/types/task.d.ts'
import { http } from '@/lib/http'

export async function getAllTasks(): Promise<Task[]> {
  return await http('/api/tasks')
}

export async function createTask(data: TaskGenerateRequest): Promise<Task> {
  // 后端 TaskCreate 需要的完整字段，这里为简化使用固定的 Prompt 文件路径，
  // 实际运行时如果你关闭了 AI 分析（SKIP_AI_ANALYSIS=true），这些文件不会被真正用到。
  const payload = {
    task_name: data.task_name,
    enabled: true,
    keyword: data.keyword,
    description: data.description || '',
    max_pages: data.max_pages ?? 3,
    personal_only: data.personal_only ?? true,
    min_price: data.min_price ?? null,
    max_price: data.max_price ?? null,
    cron: data.cron ?? null,
    ai_prompt_base_file: 'prompts/base_prompt.txt',
    ai_prompt_criteria_file: 'prompts/test_criteria.txt',
    account_state_file: data.account_state_file ?? null,
  }

  const result = await http('/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
  return result.task
}

export async function updateTask(taskId: number, data: TaskUpdate): Promise<Task> {
  const result = await http(`/api/tasks/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  return result.task
}

export async function startTask(taskId: number): Promise<void> {
  await http(`/api/tasks/start/${taskId}`, { method: 'POST' })
}

export async function stopTask(taskId: number): Promise<void> {
  await http(`/api/tasks/stop/${taskId}`, { method: 'POST' })
}

export async function deleteTask(taskId: number): Promise<void> {
  await http(`/api/tasks/${taskId}`, { method: 'DELETE' })
}

