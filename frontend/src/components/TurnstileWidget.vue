<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue"

const props = defineProps<{
  siteKey: string
  resetKey?: number
}>()

const emit = defineEmits<{
  token: [value: string]
  expired: []
  error: []
}>()

const contenedor = ref<HTMLElement | null>(null)
let widgetId: string | null = null
let scriptCargando: Promise<void> | null = null

declare global {
  interface Window {
    turnstile?: {
      render: (
        el: HTMLElement,
        options: {
          sitekey: string
          callback: (token: string) => void
          "expired-callback"?: () => void
          "error-callback"?: () => void
        },
      ) => string
      reset: (id?: string) => void
      remove: (id?: string) => void
    }
  }
}

const cargarScript = () => {
  if (window.turnstile) return Promise.resolve()
  if (scriptCargando) return scriptCargando
  scriptCargando = new Promise((resolve, reject) => {
    const existente = document.querySelector<HTMLScriptElement>("script[data-turnstile]")
    if (existente) {
      existente.addEventListener("load", () => resolve())
      existente.addEventListener("error", () => reject(new Error("Turnstile no cargó")))
      return
    }
    const script = document.createElement("script")
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"
    script.async = true
    script.dataset.turnstile = "1"
    script.onload = () => resolve()
    script.onerror = () => reject(new Error("Turnstile no cargó"))
    document.head.appendChild(script)
  })
  return scriptCargando
}

const montar = async () => {
  if (!contenedor.value || !props.siteKey) return
  await cargarScript()
  if (!window.turnstile || !contenedor.value) return
  if (widgetId !== null) {
    window.turnstile.remove(widgetId)
    widgetId = null
  }
  widgetId = window.turnstile.render(contenedor.value, {
    sitekey: props.siteKey,
    callback: (token: string) => emit("token", token),
    "expired-callback": () => {
      emit("token", "")
      emit("expired")
    },
    "error-callback": () => {
      emit("token", "")
      emit("error")
    },
  })
}

const resetear = () => {
  if (widgetId !== null && window.turnstile) {
    window.turnstile.reset(widgetId)
  }
  emit("token", "")
}

watch(
  () => props.resetKey,
  () => {
    resetear()
  },
)

onMounted(() => {
  void montar()
})

onBeforeUnmount(() => {
  if (widgetId !== null && window.turnstile) {
    window.turnstile.remove(widgetId)
    widgetId = null
  }
})

defineExpose({ resetear })
</script>

<template>
  <div ref="contenedor" class="my-3.5 min-h-[65px]" data-testid="turnstile" />
</template>
