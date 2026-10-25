<script setup lang="ts">
import Icon from "@/components/Icon.vue"

defineProps<{
  nombre: string
  descripcion: string
  imagen?: string | null
  selected?: boolean
}>()

const initial = (nombre: string) => nombre.trim().slice(-1).toUpperCase()
</script>

<template>
  <button
    type="button"
    class="flex w-full items-center gap-3.5 rounded-[20px] border p-3 text-left transition duration-200"
    :class="
      selected
        ? 'border-gold bg-linear-to-[160deg] from-[#3a2c1e] to-[#1d1710] shadow-[0_0_0_1px_var(--color-gold),0_12px_30px_#e2b75f26]'
        : 'border-ln bg-linear-to-[160deg] from-s2 to-s1'
    "
  >
    <div
      class="grid size-[60px] shrink-0 place-items-center overflow-hidden rounded-2xl bg-linear-to-br from-gold-2 to-ember font-serif text-[28px] font-semibold text-ink"
    >
      <img v-if="imagen" :src="imagen" :alt="nombre" class="size-full object-cover" />
      <span v-else>{{ initial(nombre) }}</span>
    </div>
    <div class="min-w-0 flex-1">
      <b class="block font-serif text-[17px] leading-[1.2] font-semibold">{{ nombre }}</b>
      <small class="block text-[12.5px] text-mut">{{ descripcion }}</small>
    </div>
    <span
      class="grid size-6 shrink-0 place-items-center rounded-full border-2 text-ink"
      :class="selected ? 'border-gold bg-gold' : 'border-white/25'"
    >
      <Icon name="check" :size="14" :class="selected ? 'opacity-100' : 'opacity-0'" />
    </span>
  </button>
</template>
