<script setup lang="ts">
import type { ResultItem } from '@/types/result.d.ts'
import ResultCard from './ResultCard.vue'

interface Props {
  results: ResultItem[]
  isLoading: boolean
}

defineProps<Props>()
</script>

<template>
  <div>
    <div v-if="isLoading" class="text-center py-12 text-gray-500">
      正在加载结果...
    </div>
    <div v-else-if="results.length === 0" class="text-center py-12 text-gray-500">
      没有找到符合条件的商品记录。
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ResultCard v-for="item in results" :key="item.商品信息.商品ID" :item="item" />
    </div>
  </div>
</template>
