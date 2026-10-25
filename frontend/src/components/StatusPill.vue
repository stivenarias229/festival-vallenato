<script setup lang="ts">
const props = defineProps<{
  estado: string
}>()

const label = props.estado === "proxima" ? "próxima" : props.estado
const tone =
  props.estado === "abierta" ? "text-jade" : props.estado === "proxima" ? "text-gold" : "text-mut"
</script>

<template>
  <span
    class="mt-1.5 inline-flex items-center gap-1.5 rounded-full border border-current px-2.5 py-1 text-[10px] font-extrabold tracking-[0.1em] uppercase"
    :class="tone"
  >
    <span class="size-1.5 rounded-full bg-current" aria-hidden="true" />
    {{ label }}
  </span>
</template>
