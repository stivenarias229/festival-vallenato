<script setup lang="ts">
defineProps<{
  active?: boolean
}>()
</script>

<template>
  <button
    type="button"
    class="min-h-11 shrink-0 rounded-full border px-3.5 py-2 text-xs font-bold whitespace-nowrap"
    :class="
      active
        ? 'border-gold bg-gold text-ink'
        : 'border-ln bg-white/5 text-mut'
    "
  >
    <slot />
  </button>
</template>
