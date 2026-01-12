<script setup lang="ts">
import TheHeader from '@/components/layout/TheHeader.vue'
import TheSidebar from '@/components/layout/TheSidebar.vue'
</script>

<template>
  <div class="h-screen w-full flex flex-col bg-gray-100">
    <TheHeader />
    <div class="flex flex-grow overflow-hidden">
      <TheSidebar />
      <main class="flex-grow p-6 overflow-y-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
