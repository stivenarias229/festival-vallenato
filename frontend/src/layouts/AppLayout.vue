<script setup lang="ts">
import BottomNav from "@/components/BottomNav.vue"
import FlashMessage from "@/components/FlashMessage.vue"
import TopNav from "@/components/TopNav.vue"
</script>

<template>
  <div class="relative min-h-svh bg-night text-ivory">
    <div class="aurora pointer-events-none fixed inset-0" aria-hidden="true" />
    <div
      class="app-halo relative mx-auto flex min-h-svh w-full max-w-[440px] flex-col shadow-[0_0_0_1px_var(--color-ln)] lg:max-w-6xl"
    >
      <div class="hidden items-center justify-between px-6 pt-4 lg:flex">
        <p class="font-serif text-lg font-semibold text-gold-2">Leyenda 2027</p>
        <TopNav />
      </div>
      <FlashMessage />
      <div class="flex min-h-0 flex-1 flex-col">
        <slot />
      </div>
      <BottomNav class="lg:hidden" />
    </div>
  </div>
</template>
