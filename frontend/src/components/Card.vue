<script setup lang="ts">
defineProps<{
  interactive?: boolean
  disabled?: boolean
}>()
</script>

<template>
  <div
    class="card-line relative overflow-hidden rounded-[20px] border border-ln bg-linear-to-[160deg] from-s2 to-s1"
    :class="[
      interactive && !disabled && 'transition duration-200 hover:-translate-y-0.5 hover:border-gold/40',
      disabled && 'pointer-events-none opacity-50',
    ]"
  >
    <slot />
  </div>
</template>
