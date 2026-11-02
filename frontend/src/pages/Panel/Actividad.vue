<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"
import Column from "primevue/column"
import DataTable from "primevue/datatable"

import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import { useTablaServidor, type ConsultaTabla, type PaginacionTabla } from "@/composables/useTablaServidor"

type Registro = {
  id: number
  accion: string
  entidad_afectada: string
  detalle: string
  fecha_hora: string
  usuario: string
  email: string
}

const props = defineProps<{
  actividad: Registro[]
  paginacion: PaginacionTabla
  consulta: ConsultaTabla
}>()

const page = usePage()
const {
  cargando,
  q,
  first,
  sortField,
  sortOrder,
  buscar,
  onPage,
  onSort,
  hrefExportar,
  filtrar,
  valoresFiltro,
} = useTablaServidor({
  url: () => page.props.urls.panel_actividad,
  only: ["actividad", "paginacion", "consulta"],
  consulta: () => props.consulta,
  paginacion: () => props.paginacion,
  filtros: ["accion", "entidad_afectada"],
  filtrosTexto: ["accion", "entidad_afectada"],
})

const formatearFecha = (iso: string) =>
  new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "short" }).format(new Date(iso))
</script>

<template>
  <Head title="Actividad" />
  <PageHeader title="Actividad" :back-href="page.props.urls.panel" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <div class="flex min-w-0 flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div class="barra-listado min-w-0 flex-1">
        <input
          :value="q"
          class="field barra-filtro"
          type="search"
          placeholder="Buscar"
          aria-label="Buscar"
          @input="buscar(($event.target as HTMLInputElement).value)"
        />
        <input
          class="field barra-filtro"
          type="search"
          placeholder="Acción"
          aria-label="Filtrar por acción"
          :value="valoresFiltro.accion"
          @input="filtrar('accion', ($event.target as HTMLInputElement).value)"
        />
        <input
          class="field barra-filtro"
          type="search"
          placeholder="Entidad"
          aria-label="Filtrar por entidad"
          :value="valoresFiltro.entidad_afectada"
          @input="filtrar('entidad_afectada', ($event.target as HTMLInputElement).value)"
        />
      </div>
      <div class="flex shrink-0 flex-wrap gap-2">
        <a class="mini" :href="hrefExportar(page.props.urls.panel_actividad_exportar, 'csv')">CSV</a>
        <a class="mini" :href="hrefExportar(page.props.urls.panel_actividad_exportar, 'xlsx')">Excel</a>
      </div>
    </div>
    <DataTable
      class="mt-4"
      :value="actividad"
      lazy
      paginator
      data-key="id"
      scrollable
      removable-sort
      table-style="min-width: 760px"
      :rows="paginacion.per_page"
      :first="first"
      :total-records="paginacion.count"
      :rows-per-page-options="[10, 25, 50]"
      :loading="cargando"
      :sort-field="sortField"
      :sort-order="sortOrder"
      current-page-report-template="{first}–{last} de {totalRecords}"
      paginator-template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown CurrentPageReport"
      @page="onPage"
      @sort="onSort"
    >
      <template #empty>No hay resultados.</template>
      <Column field="fecha_hora" header="Fecha" sortable>
        <template #body="{ data }">{{ formatearFecha(data.fecha_hora) }}</template>
      </Column>
      <Column field="accion" header="Acción" sortable />
      <Column field="entidad_afectada" header="Entidad" sortable />
      <Column field="usuario" header="Quién" sortable>
        <template #body="{ data }">
          <span class="block">{{ data.usuario }}</span>
          <span class="text-mut">{{ data.email }}</span>
        </template>
      </Column>
      <Column field="detalle" header="Detalle" />
    </DataTable>
  </main>
</template>
