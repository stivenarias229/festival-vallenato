<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"

import EmptyState from "@/components/EmptyState.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import StepIndicator from "@/components/StepIndicator.vue"
import VotingCard from "@/components/VotingCard.vue"

defineProps<{
  categoria: { id: number; nombre: string }
  votaciones: Array<{
    id: number
    titulo: string
    resumen_fecha: string
    estado_efectivo: string
  }>
}>()

const page = usePage()
</script>

<template>
  <Head :title="categoria.nombre" />
  <PageHeader :title="categoria.nombre" :back-href="page.props.urls.categorias" />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <StepIndicator :current="1" />
    <EmptyState
      v-if="!votaciones.length"
      titulo="No hay votaciones en esta categoría"
      descripcion="Vuelve más tarde o elige otra categoría."
    />
    <div v-else class="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
      <VotingCard
        v-for="votacion in votaciones"
        :key="votacion.id"
        :href="votacion.estado_efectivo === 'abierta' ? `/votaciones/${votacion.id}` : undefined"
        :titulo="votacion.titulo"
        :resumen="votacion.resumen_fecha"
        :estado="votacion.estado_efectivo"
      />
    </div>
  </main>
</template>
