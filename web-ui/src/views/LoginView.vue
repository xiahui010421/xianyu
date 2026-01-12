<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const { login } = useAuth()
const router = useRouter()
const route = useRoute()

async function handleLogin() {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const success = await login(username.value, password.value)
    if (success) {
      const redirectPath = (route.query.redirect as string) || '/'
      router.push(redirectPath)
    } else {
      error.value = '登录失败：用户名或密码错误'
    }
  } catch (e) {
    error.value = '登录过程中发生错误'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <Card class="w-full max-w-md">
      <CardHeader>
        <CardTitle class="text-2xl text-center">系统登录</CardTitle>
        <CardDescription class="text-center">
          请输入您的管理员凭证以继续
        </CardDescription>
      </CardHeader>
      <form @submit.prevent="handleLogin">
        <CardContent class="grid gap-4">
          <div class="grid gap-2">
            <Label for="username">用户名</Label>
            <Input id="username" type="text" v-model="username" placeholder="admin" required />
          </div>
          <div class="grid gap-2">
            <Label for="password">密码</Label>
            <Input id="password" type="password" v-model="password" required />
          </div>
          <div v-if="error" class="text-sm text-red-500 font-medium">
            {{ error }}
          </div>
        </CardContent>
        <CardFooter>
          <Button class="w-full" type="submit" :disabled="isLoading">
            {{ isLoading ? '登录中...' : '登录' }}
          </Button>
        </CardFooter>
      </form>
    </Card>
  </div>
</template>
