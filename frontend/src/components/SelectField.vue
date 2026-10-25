<script setup lang="ts">
import { computed, nextTick, onUnmounted, ref, useId } from "vue"

import Icon from "@/components/Icon.vue"

export type SelectOption = { value: string | number; label: string }

const model = defineModel<string | number | null>({ default: null })

const props = withDefaults(
  defineProps<{
    options: SelectOption[]
    disabled?: boolean
    placeholder?: string
    compact?: boolean
    id?: string
  }>(),
  { disabled: false, placeholder: "Selecciona", compact: false },
)

const listId = useId()
const abierto = ref(false)
const disparador = ref<HTMLButtonElement | null>(null)
const coords = ref({ top: 0, left: 0, width: 220 })

const etiqueta = computed(
  () => props.options.find((opcion) => String(opcion.value) === String(model.value))?.label ?? props.placeholder,
)

const posicionar = () => {
  const rect = disparador.value?.getBoundingClientRect()
  if (!rect) return
  coords.value = {
    top: rect.bottom + 6,
    left: rect.left,
    width: Math.max(rect.width, 240),
  }
}

const cerrar = () => {
  abierto.value = false
  document.removeEventListener("mousedown", onClickFuera)
  window.removeEventListener("resize", cerrar)
  window.removeEventListener("scroll", cerrar, true)
}

const onClickFuera = (evento: MouseEvent) => {
  const destino = evento.target as Node
  if (disparador.value?.contains(destino)) return
  if ((destino as HTMLElement).closest?.(`[data-select-list="${listId}"]`)) return
  cerrar()
}

const abrir = async () => {
  if (props.disabled) return
  abierto.value = true
  await nextTick()
  posicionar()
  document.addEventListener("mousedown", onClickFuera)
  window.addEventListener("resize", cerrar)
  window.addEventListener("scroll", cerrar, true)
}

const alternar = () => {
  if (abierto.value) {
    cerrar()
    return
  }
  void abrir()
}

const elegir = (opcion: SelectOption) => {
  model.value = opcion.value
  cerrar()
}

onUnmounted(cerrar)
</script>

<template>
  <div class="relative">
    <button
      :id="id"
      ref="disparador"
      type="button"
      class="field flex items-center justify-between gap-2 text-left disabled:pointer-events-none disabled:opacity-35"
      :class="compact ? 'w-auto min-w-[11rem] py-2 text-xs' : 'w-full'"
      :disabled="disabled"
      :aria-expanded="abierto"
      :aria-controls="listId"
      aria-haspopup="listbox"
      @click="alternar"
    >
      <span class="min-w-0 truncate">{{ etiqueta }}</span>
      <Icon
        name="chevron"
        :size="compact ? 14 : 18"
        class="shrink-0 text-gold transition-transform"
        :class="abierto ? '-rotate-90' : 'rotate-90'"
      />
    </button>
    <Teleport to="body">
      <div
        v-if="abierto"
        :id="listId"
        :data-select-list="listId"
        role="listbox"
        class="fixed z-40 max-h-64 overflow-y-auto rounded-2xl border border-gold/35 bg-s2 p-1.5 shadow-[0_18px_40px_#00000099]"
        :style="{ top: `${coords.top}px`, left: `${coords.left}px`, width: `${coords.width}px` }"
      >
        <button
          v-for="opcion in options"
          :key="String(opcion.value)"
          type="button"
          role="option"
          class="flex min-h-11 w-full items-center rounded-xl px-3 py-2 text-left text-[15px] font-semibold text-ivory hover:bg-gold/15"
          :class="String(opcion.value) === String(model) ? 'bg-gold/20 text-gold-2' : ''"
          :aria-selected="String(opcion.value) === String(model)"
          @click="elegir(opcion)"
        >
          {{ opcion.label }}
        </button>
      </div>
    </Teleport>
  </div>
</template>
