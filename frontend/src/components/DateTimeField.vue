<script setup lang="ts">
import { computed, ref } from "vue"

import Icon from "@/components/Icon.vue"

const model = defineModel<string>({ default: "" })

const props = withDefaults(
  defineProps<{
    placeholder?: string
    disabled?: boolean
    id?: string
  }>(),
  { placeholder: "Elige fecha y hora", disabled: false },
)

const nativo = ref<HTMLInputElement | null>(null)

const etiqueta = computed(() => formatearFechaHora(model.value) || props.placeholder)

const abrir = () => {
  if (props.disabled) return
  try {
    nativo.value?.showPicker?.()
  } catch {
    nativo.value?.focus()
  }
}

function formatearFechaHora(valor: string) {
  if (!valor) return ""
  const [fecha, hora = "00:00"] = valor.split("T")
  const partes = fecha.split("-").map(Number)
  if (partes.length < 3 || partes.some((parte) => Number.isNaN(parte))) return ""
  const [anio, mes, dia] = partes
  const [horas, minutos] = hora.split(":").map(Number)
  const local = new Date(anio, mes - 1, dia, horas || 0, minutos || 0)
  if (Number.isNaN(local.getTime())) return ""
  return new Intl.DateTimeFormat("es-CO", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(local)
}
</script>

<template>
  <div
    :id="id"
    data-testid="datetime-field"
    role="button"
    tabindex="0"
    :aria-label="placeholder"
    class="field relative flex cursor-pointer items-center justify-between gap-3"
    :class="disabled ? 'pointer-events-none opacity-35' : ''"
    @click="abrir"
    @keydown.enter.prevent="abrir"
    @keydown.space.prevent="abrir"
  >
    <span class="pointer-events-none min-w-0 truncate font-semibold" :class="model ? 'text-ivory' : 'text-mut'">
      {{ etiqueta }}
    </span>
    <span class="pointer-events-none grid size-9 shrink-0 place-items-center rounded-xl bg-gold/15 text-gold">
      <Icon name="calendar" :size="18" />
    </span>
    <input
      ref="nativo"
      type="datetime-local"
      class="pointer-events-none absolute inset-0 opacity-0"
      tabindex="-1"
      :disabled="disabled"
      :value="model"
      :aria-label="placeholder"
      @input="model = ($event.target as HTMLInputElement).value"
      @change="model = ($event.target as HTMLInputElement).value"
    />
  </div>
</template>
