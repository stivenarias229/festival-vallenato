<script setup lang="ts">
import BottomNav from "@/components/BottomNav.vue"
import FlashMessage from "@/components/FlashMessage.vue"
import SidebarNav from "@/components/SidebarNav.vue"
</script>

<template>
  <div class="relative min-h-svh bg-night text-ivory">
    <div class="aurora pointer-events-none fixed inset-0" aria-hidden="true" />
    <div class="relative mx-auto flex min-h-svh w-full max-w-[440px] lg:max-w-none">
      <SidebarNav />
      <div class="app-halo flex min-h-svh min-w-0 flex-1 flex-col">
        <FlashMessage />
        <div class="flex min-h-0 flex-1 flex-col">
          <slot />
        </div>
        <BottomNav admin class="lg:hidden" />
      </div>
    </div>
  </div>
</template>
