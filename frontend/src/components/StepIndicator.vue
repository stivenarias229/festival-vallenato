<script setup lang="ts">
const steps = ["Categoría", "Votación", "Opción", "Confirmar"]

defineProps<{
  current: number
}>()
</script>

<template>
  <ol class="mb-4 flex gap-1.5" aria-label="Progreso de votación">
    <li
      v-for="(step, index) in steps"
      :key="step"
      class="flex-1 border-t-[3px] pt-2 text-[9.5px] font-extrabold tracking-[0.1em] uppercase"
      :class="index <= current ? 'border-gold text-gold' : 'border-white/10 text-[#6f6580]'"
      :aria-current="index === current ? 'step' : undefined"
    >
      {{ index + 1 }} · {{ step }}
    </li>
  </ol>
</template>
