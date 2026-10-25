<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import EmptyState from "@/components/EmptyState.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import ResultBar from "@/components/ResultBar.vue"

defineProps<{
  votacion: { id: number; titulo: string }
  disponible: boolean
  resultados: { total: number; opciones: Array<{ nombre: string; porcentaje: number; votos: number }> }
}>()

const page = usePage()
</script>

<template>
  <Head title="Resultados" />
  <PageHeader title="Resultados" :back-href="`/votaciones/${votacion.id}`" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-xl flex-1 px-[18px] pt-4 pb-8">
    <h2 class="mb-4 font-serif text-2xl font-semibold">{{ votacion.titulo }}</h2>
    <EmptyState
      v-if="!disponible"
      titulo="Resultados no disponibles"
      descripcion="El Festival aún no publica estos resultados para el público."
    />
    <template v-else>
      <EmptyState v-if="!resultados.total" titulo="Todavía no hay votos" />
      <ResultBar
        v-for="opcion in resultados.opciones"
        :key="opcion.nombre"
        :nombre="opcion.nombre"
        :porcentaje="opcion.porcentaje"
        :votos="opcion.votos"
      />
    </template>
    <Button class="mt-4" :href="page.props.urls.categorias">Volver a categorías</Button>
  </main>
</template>
