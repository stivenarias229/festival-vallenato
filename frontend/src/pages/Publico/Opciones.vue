<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { ref } from "vue"
import { Head } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import OptionCard from "@/components/OptionCard.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import StepIndicator from "@/components/StepIndicator.vue"
import { useServerAction } from "@/composables/useServerAction"

const props = defineProps<{
  votacion: { id: number; titulo: string }
  opciones: Array<{
    id: number
    nombre: string
    descripcion: string
    imagen?: string | null
  }>
}>()

const seleccion = ref<number | null>(null)
const { processing, get } = useServerAction()

const continuar = () => {
  if (!seleccion.value) return
  get(`/votaciones/${props.votacion.id}/confirmar`, { opcion: seleccion.value })
}
</script>

<template>
  <Head title="Elige tu opción" />
  <PageHeader title="Elige tu opción" :back-href="`/votaciones/${votacion.id}`" />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <StepIndicator :current="2" />
    <p class="text-[10px] font-extrabold tracking-[0.18em] text-gold uppercase">{{ votacion.titulo }}</p>
    <div class="mt-2 grid gap-3 md:grid-cols-2 lg:grid-cols-3">
      <OptionCard
        v-for="opcion in opciones"
        :key="opcion.id"
        :nombre="opcion.nombre"
        :descripcion="opcion.descripcion"
        :imagen="opcion.imagen"
        :selected="seleccion === opcion.id"
        @click="seleccion = opcion.id"
      />
    </div>
    <Button class="mt-4" :disabled="!seleccion" :loading="processing" @click="continuar">
      Continuar
    </Button>
  </main>
</template>
