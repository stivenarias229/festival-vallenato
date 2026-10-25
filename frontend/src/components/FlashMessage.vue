<script setup lang="ts">
import { computed, onUnmounted, ref, watch } from "vue"
import { usePage } from "@inertiajs/vue3"

import Icon from "@/components/Icon.vue"
import type { FlashMessages } from "@/types/inertia"

type TipoToast = "success" | "error" | "info"

const DURACION: Record<TipoToast, number> = {
  success: 5500,
  error: 8000,
  info: 5500,
}

const ESTILO: Record<TipoToast, { titulo: string; icono: string; clases: string; iconoClases: string }> = {
  success: {
    titulo: "Listo",
    icono: "check",
    clases: "border-jade/50 bg-[#10241f] text-ivory shadow-[0_18px_40px_#000c,0_0_0_1px_#45bfa855]",
    iconoClases: "bg-jade/20 text-jade",
  },
  error: {
    titulo: "Error",
    icono: "alert",
    clases: "border-ember/55 bg-[#2a1210] text-ivory shadow-[0_18px_40px_#000c,0_0_0_1px_#e0573b66]",
    iconoClases: "bg-ember/20 text-ember",
  },
  info: {
    titulo: "Aviso",
    icono: "info",
    clases: "border-gold/50 bg-[#24190f] text-ivory shadow-[0_18px_40px_#000c,0_0_0_1px_#e2b75f55]",
    iconoClases: "bg-gold/15 text-gold-2",
  },
}

const props = defineProps<{
  flash?: FlashMessages
}>()

const page = usePage()
const flash = computed<FlashMessages>(() => props.flash ?? page.props.flash ?? {})
const ocultos = ref<Partial<Record<TipoToast, boolean>>>({})
const temporizadores: Partial<Record<TipoToast, number>> = {}

const toasts = computed(() =>
  (["success", "error", "info"] as const)
    .filter((tipo) => flash.value[tipo] && !ocultos.value[tipo])
    .map((tipo) => ({
      tipo,
      texto: flash.value[tipo] as string,
      ...ESTILO[tipo],
    })),
)

const limpiarTemporizadores = () => {
  for (const tipo of Object.keys(temporizadores) as TipoToast[]) {
    window.clearTimeout(temporizadores[tipo])
    delete temporizadores[tipo]
  }
}

const programarCierre = () => {
  limpiarTemporizadores()
  for (const toast of toasts.value) {
    temporizadores[toast.tipo] = window.setTimeout(() => {
      ocultos.value = { ...ocultos.value, [toast.tipo]: true }
    }, DURACION[toast.tipo])
  }
}

watch(
  flash,
  () => {
    ocultos.value = {}
    programarCierre()
  },
  { deep: true, immediate: true },
)

onUnmounted(limpiarTemporizadores)

const cerrar = (tipo: TipoToast) => {
  window.clearTimeout(temporizadores[tipo])
  delete temporizadores[tipo]
  ocultos.value = { ...ocultos.value, [tipo]: true }
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="toasts.length"
      class="pointer-events-none fixed inset-x-0 top-0 z-50 flex justify-center px-3 pt-[max(1rem,env(safe-area-inset-top))]"
      data-testid="toast-stack"
    >
      <div class="flex w-full max-w-md flex-col gap-2">
        <article
          v-for="toast in toasts"
          :key="toast.tipo"
          class="toast-enter pointer-events-auto flex items-start gap-3 rounded-2xl border px-3.5 py-3.5"
          :class="toast.clases"
          :role="toast.tipo === 'error' ? 'alert' : 'status'"
          aria-live="polite"
        >
          <span
            class="mt-0.5 grid size-11 shrink-0 place-items-center rounded-full"
            :class="toast.iconoClases"
          >
            <Icon :name="toast.icono" :size="22" />
          </span>
          <div class="min-w-0 flex-1 pt-0.5">
            <p class="text-[11px] font-extrabold tracking-[0.16em] text-gold-2 uppercase">
              {{ toast.titulo }}
            </p>
            <p class="mt-0.5 text-[15px] leading-snug font-bold">{{ toast.texto }}</p>
          </div>
          <button
            type="button"
            class="grid min-h-11 min-w-11 shrink-0 place-items-center rounded-xl text-ivory/70 hover:bg-white/5 hover:text-ivory"
            aria-label="Cerrar aviso"
            @click="cerrar(toast.tipo)"
          >
            <Icon name="close" :size="18" />
          </button>
        </article>
      </div>
    </div>
  </Teleport>
</template>
