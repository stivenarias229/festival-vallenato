<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"

import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import Pagination from "@/components/Pagination.vue"

const props = defineProps<{
  actividad: Array<{
    id: number
    accion: string
    entidad_afectada: string
    detalle: string
    fecha_hora: string
    usuario: string
    email: string
  }>
  paginacion: { number: number; num_pages: number }
}>()

const page = usePage()
const links = Array.from({ length: props.paginacion.num_pages }, (_, index) => ({
  url: `${page.props.urls.panel_actividad}?page=${index + 1}`,
  label: String(index + 1),
  active: props.paginacion.number === index + 1,
}))
</script>

<template>
  <Head title="Actividad" />
  <PageHeader title="Actividad" :back-href="page.props.urls.panel" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <div class="hidden overflow-x-auto lg:block">
      <table class="w-full text-left text-sm">
        <thead class="text-mut">
          <tr>
            <th class="p-3">Acción</th>
            <th class="p-3">Entidad</th>
            <th class="p-3">Quién</th>
            <th class="p-3">Detalle</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in actividad" :key="item.id" class="border-t border-ln">
            <td class="p-3">{{ item.accion }}</td>
            <td class="p-3">{{ item.entidad_afectada }}</td>
            <td class="p-3">{{ item.usuario }}</td>
            <td class="p-3 text-mut">{{ item.detalle }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="lg:hidden">
      <div
        v-for="item in actividad"
        :key="item.id"
        class="my-2.5 rounded-2xl border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-3.5 py-3"
      >
        <b class="block font-serif text-[17px] font-semibold">{{ item.accion }}</b>
        <small class="text-mut">{{ item.usuario }} · {{ item.entidad_afectada }}</small>
        <p class="mt-1 text-[13px] text-mut">{{ item.detalle }}</p>
      </div>
    </div>
    <Pagination :links="links" />
  </main>
</template>
