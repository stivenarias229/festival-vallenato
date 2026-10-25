<script setup lang="ts">
withDefaults(defineProps<{ size?: number }>(), { size: 20 })
</script>

<template>
  <span
    data-testid="loader"
    class="inline-block animate-spin rounded-full border-2 border-current border-t-transparent"
    :style="{ width: `${size}px`, height: `${size}px` }"
    aria-hidden="true"
  />
</template>
