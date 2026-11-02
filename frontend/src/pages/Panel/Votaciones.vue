<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { ref } from "vue"
import { Head, Link, useForm, usePage } from "@inertiajs/vue3"
import Column from "primevue/column"
import DataTable from "primevue/datatable"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import DateTimeField from "@/components/DateTimeField.vue"
import FormField from "@/components/FormField.vue"
import SelectField from "@/components/SelectField.vue"
import StatusPill from "@/components/StatusPill.vue"
import { useServerAction } from "@/composables/useServerAction"
import { useTablaServidor, type ConsultaTabla, type PaginacionTabla } from "@/composables/useTablaServidor"

const filtroEstado = [
  { value: "", label: "Todos" },
  { value: "borrador", label: "Borrador" },
  { value: "proxima", label: "Próxima" },
  { value: "abierta", label: "Abierta" },
  { value: "cerrada", label: "Cerrada" },
]

type Votacion = {
  id: number
  titulo: string
  categoria_id: number
  categoria_nombre: string
  fecha_inicio: string
  fecha_fin: string
  estado: string
  estado_efectivo: string
  reglas: string
  visibilidad_resultados: string
  limite_votos_por_usuario: number
  resumen_fecha: string
  opciones_count: number
}

const props = defineProps<{
  categorias: Array<{ id: number; nombre: string }>
  votaciones: Votacion[]
  paginacion: PaginacionTabla
  consulta: ConsultaTabla
}>()

const page = usePage()
const mostrar = ref(false)
const form = useForm({
  accion: "guardar",
  id: "",
  categoria: props.categorias[0]?.id ?? "",
  titulo: "",
  fecha_inicio: "",
  fecha_fin: "",
  estado: "borrador",
  reglas: "",
  visibilidad_resultados: "internos",
  limite_votos_por_usuario: 1,
})

const editar = (votacion: Votacion) => {
  form.id = String(votacion.id)
  form.categoria = votacion.categoria_id
  form.titulo = votacion.titulo
  form.fecha_inicio = votacion.fecha_inicio.slice(0, 16)
  form.fecha_fin = votacion.fecha_fin.slice(0, 16)
  form.estado = votacion.estado
  form.reglas = votacion.reglas
  form.visibilidad_resultados = votacion.visibilidad_resultados
  form.limite_votos_por_usuario = votacion.limite_votos_por_usuario
  mostrar.value = true
}

const { processing: accionProcessing, isBusy, post } = useServerAction()
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
} = useTablaServidor({
  url: () => page.props.urls.panel_votaciones,
  only: ["votaciones", "paginacion", "consulta"],
  consulta: () => props.consulta,
  paginacion: () => props.paginacion,
  filtros: ["estado"],
  filtrosTexto: [],
})

const cambiarEstado = (id: number, accion: "abrir" | "cerrar") => {
  post(page.url, { accion, id }, `estado-${id}`)
}
</script>

<template>
  <Head title="Votaciones" />
  <PageHeader title="Votaciones" :back-href="page.props.urls.panel" admin />
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
        <SelectField
          class="barra-filtro"
          aria-label="Filtrar por estado"
          :model-value="consulta.filtros.estado ?? ''"
          :options="filtroEstado"
          @update:model-value="(valor) => filtrar('estado', valor)"
        />
      </div>
      <div class="flex shrink-0 flex-wrap gap-2">
        <a class="mini" :href="hrefExportar(page.props.urls.panel_votaciones_exportar, 'csv')">CSV</a>
        <a class="mini" :href="hrefExportar(page.props.urls.panel_votaciones_exportar, 'xlsx')">Excel</a>
      </div>
    </div>
    <DataTable
      class="mt-4"
      :value="votaciones"
      lazy
      paginator
      data-key="id"
      scrollable
      removable-sort
      table-style="min-width: 860px"
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
      <Column field="titulo" header="Título" sortable>
        <template #body="{ data }">
          <span class="font-serif">{{ data.titulo }}</span>
        </template>
      </Column>
      <Column field="categoria" header="Categoría" sortable>
        <template #body="{ data }">{{ data.categoria_nombre }}</template>
      </Column>
      <Column field="fecha_inicio" header="Fechas" sortable>
        <template #body="{ data }">{{ data.resumen_fecha }}</template>
      </Column>
      <Column field="estado" header="Estado" sortable>
        <template #body="{ data }">
          <StatusPill :estado="data.estado_efectivo" />
        </template>
      </Column>
      <Column field="opciones_count" header="Opciones">
        <template #body="{ data }">{{ data.opciones_count }}</template>
      </Column>
      <Column header="Acciones">
        <template #body="{ data }">
          <div class="flex flex-wrap gap-2">
            <Link class="mini" :href="`${page.props.urls.panel_votaciones}/${data.id}/opciones`">Opciones</Link>
            <button type="button" class="mini" @click="editar(data)">Editar</button>
            <Button
              size="mini"
              variant="secondary"
              :loading="isBusy(`estado-${data.id}`)"
              :disabled="accionProcessing"
              @click="cambiarEstado(data.id, data.estado === 'abierta' ? 'cerrar' : 'abrir')"
            >
              {{ data.estado === "abierta" ? "Cerrar" : "Abrir" }}
            </Button>
          </div>
        </template>
      </Column>
    </DataTable>
    <Button class="mt-4" @click="mostrar = !mostrar">
      <Icon name="plus" :size="18" />
      Nueva votación
    </Button>
    <form v-if="mostrar" class="mt-4 grid gap-3" @submit.prevent="form.post(page.url)">
      <FormField compact label="Categoría" for-id="votacion-categoria">
        <SelectField
          id="votacion-categoria"
          v-model="form.categoria"
          :options="categorias.map((categoria) => ({ value: categoria.id, label: categoria.nombre }))"
        />
      </FormField>
      <FormField compact label="Título" for-id="votacion-titulo">
        <input id="votacion-titulo" v-model="form.titulo" class="field" placeholder="Ej. Canción favorita" />
      </FormField>
      <FormField compact label="Fecha de inicio" for-id="votacion-inicio">
        <DateTimeField id="votacion-inicio" v-model="form.fecha_inicio" placeholder="Elige fecha y hora" />
      </FormField>
      <FormField compact label="Fecha de cierre" for-id="votacion-cierre">
        <DateTimeField id="votacion-cierre" v-model="form.fecha_fin" placeholder="Elige fecha y hora" />
      </FormField>
      <FormField compact label="Reglas" for-id="votacion-reglas">
        <textarea id="votacion-reglas" v-model="form.reglas" class="field" rows="4" placeholder="Condiciones de la votación" />
      </FormField>
      <FormField compact label="Visibilidad de resultados" for-id="votacion-visibilidad">
        <SelectField
          id="votacion-visibilidad"
          v-model="form.visibilidad_resultados"
          :options="[
            { value: 'internos', label: 'Internos' },
            { value: 'al_cierre', label: 'Al cierre' },
            { value: 'en_vivo', label: 'En vivo' },
          ]"
        />
      </FormField>
      <FormField compact label="Límite de votos por usuario" for-id="votacion-limite">
        <input id="votacion-limite" v-model.number="form.limite_votos_por_usuario" class="field" type="number" min="1" />
      </FormField>
      <Button type="submit" :loading="form.processing">Guardar votación</Button>
    </form>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Reglas, fechas y visibilidad de resultados configurables por votación (RF-07).
    </p>
  </main>
</template>
