<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    error?: string
    forId?: string
    compact?: boolean
  }>(),
  { compact: false },
)
</script>

<template>
  <div :class="compact ? '' : 'my-3.5'">
    <label
      :for="forId"
      class="mb-1.5 block text-[11px] font-extrabold tracking-[0.1em] text-mut uppercase"
    >
      {{ label }}
    </label>
    <slot />
    <p v-if="error" class="mt-1.5 text-[13px] text-ember" role="alert">{{ error }}</p>
  </div>
</template>
