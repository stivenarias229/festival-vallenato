<script setup lang="ts">
import Chip from "@/components/Chip.vue"
import Icon from "@/components/Icon.vue"

const props = defineProps<{
  q: string
  filtro: string
}>()

const emit = defineEmits<{
  buscar: [value: string]
  filtrar: [value: string]
}>()

const chips = [
  { id: "todos", label: "Todos" },
  { id: "votante", label: "Votantes" },
  { id: "administrador", label: "Admins" },
  { id: "bloqueados", label: "Bloqueados" },
]
</script>

<template>
  <div>
    <div class="relative">
      <Icon name="search" :size="18" class="absolute top-1/2 left-3.5 -translate-y-1/2 text-mut" />
      <input
        :value="props.q"
        class="field pl-[42px]"
        type="search"
        placeholder="Buscar por nombre o correo"
        @input="emit('buscar', ($event.target as HTMLInputElement).value)"
      />
    </div>
    <div class="mt-3 flex gap-2 overflow-x-auto">
      <Chip
        v-for="chip in chips"
        :key="chip.id"
        :active="filtro === chip.id"
        @click="emit('filtrar', chip.id)"
      >
        {{ chip.label }}
      </Chip>
    </div>
  </div>
</template>
