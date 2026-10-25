<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"

import CategoryCard from "@/components/CategoryCard.vue"
import EmptyState from "@/components/EmptyState.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import StepIndicator from "@/components/StepIndicator.vue"

defineProps<{
  categorias: Array<{
    id: number
    nombre: string
    descripcion: string
    icono: string
  }>
}>()

const page = usePage()
</script>

<template>
  <Head title="Categorías" />
  <PageHeader title="Elige una categoría" :back-href="page.props.urls.inicio" />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <StepIndicator :current="0" />
    <EmptyState
      v-if="!categorias.length"
      titulo="No hay categorías disponibles"
      descripcion="Cuando la organización publique la edición activa aparecerán aquí."
    />
    <div v-else class="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
      <CategoryCard
        v-for="categoria in categorias"
        :key="categoria.id"
        :href="`/categorias/${categoria.id}/votaciones`"
        :icono="categoria.icono"
        :nombre="categoria.nombre"
        :descripcion="categoria.descripcion"
      />
    </div>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Datos de ejemplo: categorías, votaciones, opciones y usuarios son ilustrativos y están
      <b class="text-gold-2">pendientes de validación</b> con el cliente.
    </p>
  </main>
</template>
