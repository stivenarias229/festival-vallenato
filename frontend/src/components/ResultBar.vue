<script setup lang="ts">
defineProps<{
  nombre: string
  porcentaje: number
  votos?: number
}>()
</script>

<template>
  <div class="mb-4">
    <div class="flex items-baseline justify-between gap-3">
      <b class="font-serif text-base font-semibold">{{ nombre }}</b>
      <span class="font-extrabold text-gold-2">
        {{ porcentaje }}%
        <span v-if="votos !== undefined" class="ml-1 text-xs font-bold text-mut">{{ votos }}</span>
      </span>
    </div>
    <div class="mt-1.5 h-2.5 overflow-hidden rounded-full bg-white/10" role="img" :aria-label="`${nombre}: ${porcentaje}%`">
      <i
        class="block h-full rounded-full bg-linear-to-r from-ember to-gold"
        :style="{ width: `${Math.max(0, Math.min(100, porcentaje))}%` }"
      />
    </div>
  </div>
</template>
