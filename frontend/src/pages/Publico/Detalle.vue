<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import StatusPill from "@/components/StatusPill.vue"
import StepIndicator from "@/components/StepIndicator.vue"

const props = defineProps<{
  votacion: {
    id: number
    titulo: string
    resumen_fecha: string
    estado_efectivo: string
    reglas: string
    categoria_id: number
  }
  categoria: { id: number; nombre: string }
}>()

const reglas = props.votacion.reglas
  .split("\n")
  .map((linea) => linea.trim())
  .filter(Boolean)
</script>

<template>
  <Head title="Detalle" />
  <PageHeader title="Detalle" :back-href="`/categorias/${votacion.categoria_id}/votaciones`" />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <StepIndicator :current="1" />
    <div class="card-line relative overflow-hidden rounded-[20px] border border-ln bg-linear-to-[160deg] from-s2 to-s1 p-4">
      <h2 class="font-serif text-[26px] leading-[1.15] font-semibold">{{ votacion.titulo }}</h2>
      <StatusPill :estado="votacion.estado_efectivo" />
      <p class="mt-2.5 text-mut">
        {{ votacion.resumen_fecha }}. Elige tu favorito entre las opciones participantes.
      </p>
    </div>
    <h3 class="mt-6 mb-2 font-serif text-xl font-semibold">Reglas</h3>
    <ul class="list-none p-0 text-[13.5px] text-mut">
      <li
        v-for="regla in reglas"
        :key="regla"
        class="relative border-b border-ln py-2.5 pr-0 pl-[22px] before:absolute before:top-[17px] before:left-0.5 before:size-[7px] before:rotate-45 before:bg-gold before:content-['']"
      >
        {{ regla }}
      </li>
    </ul>
    <Button
      v-if="votacion.estado_efectivo === 'abierta'"
      class="mt-4"
      :href="`/votaciones/${votacion.id}/opciones`"
    >
      Ver opciones
      <Icon name="chevron" :size="20" />
    </Button>
  </main>
</template>
