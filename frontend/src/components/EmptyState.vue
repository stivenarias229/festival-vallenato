<script setup lang="ts">
defineProps<{
  titulo: string
  descripcion?: string
}>()
</script>

<template>
  <div class="rounded-[20px] border border-dashed border-gold/35 bg-gold/5 px-4 py-8 text-center">
    <p class="font-serif text-lg font-semibold">{{ titulo }}</p>
    <p v-if="descripcion" class="mt-2 text-[13px] text-mut">{{ descripcion }}</p>
    <slot />
  </div>
</template>
