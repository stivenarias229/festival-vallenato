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

defineProps<{
  votos: Array<{
    id: number
    fecha_hora: string
    categoria: { id: number; nombre: string }
    votacion: { id: number; titulo: string }
    opcion: { id: number; nombre: string }
  }>
}>()

const page = usePage()

const formatearFecha = (iso: string) => {
  const fecha = new Date(iso)
  if (Number.isNaN(fecha.getTime())) return iso
  return fecha.toLocaleString("es-CO", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}
</script>

<template>
  <Head title="Mis votos" />
  <PageHeader title="Mis votos" :back-href="page.props.urls.categorias" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8 lg:max-w-3xl">
    <EmptyState
      v-if="!votos.length"
      titulo="Aún no has votado"
      descripcion="Cuando confirmes un voto en una categoría aparecerá aquí."
    >
      <div class="mt-4">
        <Button :href="page.props.urls.categorias">Ir a votar</Button>
      </div>
    </EmptyState>
    <ul v-else class="grid gap-3 md:grid-cols-2">
      <li
        v-for="voto in votos"
        :key="voto.id"
        class="rounded-[18px] border border-ln bg-linear-to-[160deg] from-s2 to-s1 p-4"
      >
        <p class="text-[11px] font-bold tracking-[0.08em] text-gold-2 uppercase">
          {{ voto.categoria.nombre }}
        </p>
        <h2 class="mt-1 font-serif text-[18px] leading-snug font-semibold">
          {{ voto.votacion.titulo }}
        </h2>
        <p class="mt-2 text-[14px] text-ivory">
          Tu opción: <b class="text-gold-2">{{ voto.opcion.nombre }}</b>
        </p>
        <p class="mt-1 text-[12px] text-mut">{{ formatearFecha(voto.fecha_hora) }}</p>
      </li>
    </ul>
    <div v-if="votos.length" class="mt-5">
      <Button variant="secondary" :href="page.props.urls.categorias">Votar en otra categoría</Button>
    </div>
  </main>
</template>
