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
import SelectField from "@/components/SelectField.vue"
import Switch from "@/components/Switch.vue"
import { useServerAction } from "@/composables/useServerAction"
import { useTablaServidor, type ConsultaTabla, type PaginacionTabla } from "@/composables/useTablaServidor"

const rolesUsuario = [
  { value: "votante", label: "Votante" },
  { value: "administrador", label: "Administrador" },
]

const filtroRol = [{ value: "", label: "Todos" }, ...rolesUsuario]
const filtroEstado = [
  { value: "", label: "Todos" },
  { value: "activo", label: "Activo" },
  { value: "bloqueado", label: "Bloqueado" },
]

type Usuario = {
  id: number
  nombre: string
  email: string
  rol: string
  estado: string
  fecha_registro: string
  tiene_votos: boolean
}

const props = defineProps<{
  usuarios: Usuario[]
  paginacion: PaginacionTabla
  consulta: ConsultaTabla
}>()

const page = usePage()
const yo = page.props.auth.user
const { processing, isBusy, post } = useServerAction()
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
  url: () => page.props.urls.panel_usuarios,
  only: ["usuarios", "paginacion", "consulta"],
  consulta: () => props.consulta,
  paginacion: () => props.paginacion,
  filtros: ["rol", "estado"],
  filtrosTexto: [],
})

const actualizar = (usuario: Usuario, cambios: Partial<Usuario>) => {
  if (yo && usuario.id === yo.id) return
  post(
    page.url,
    {
      id: usuario.id,
      rol: cambios.rol ?? usuario.rol,
      estado: cambios.estado ?? usuario.estado,
    },
    `usuario-${usuario.id}`,
  )
}
</script>

<template>
  <Head title="Usuarios" />
  <PageHeader title="Usuarios" :back-href="page.props.urls.panel" admin />
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
          aria-label="Filtrar por rol"
          :model-value="consulta.filtros.rol ?? ''"
          :options="filtroRol"
          @update:model-value="(valor) => filtrar('rol', valor)"
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
        <a class="mini" :href="hrefExportar(page.props.urls.panel_usuarios_exportar, 'csv')">CSV</a>
        <a class="mini" :href="hrefExportar(page.props.urls.panel_usuarios_exportar, 'xlsx')">Excel</a>
      </div>
    </div>
    <DataTable
      class="mt-4"
      :value="usuarios"
      lazy
      paginator
      data-key="id"
      scrollable
      removable-sort
      table-style="min-width: 720px"
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
      <Column field="nombre" header="Nombre" sortable>
        <template #body="{ data }">
          <span class="font-serif">{{ data.nombre }}</span>
        </template>
      </Column>
      <Column field="email" header="Correo" sortable />
      <Column field="rol" header="Rol" sortable>
        <template #body="{ data }">
          <SelectField
            compact
            :model-value="data.rol"
            :options="rolesUsuario"
            :disabled="yo?.id === data.id || processing"
            @update:model-value="(rol) => actualizar(data, { rol: String(rol) })"
          />
        </template>
      </Column>
      <Column field="estado" header="Estado" sortable>
        <template #body="{ data }">
          <Switch
            :model-value="data.estado === 'activo'"
            :disabled="yo?.id === data.id || processing"
            :loading="isBusy(`usuario-${data.id}`)"
            @update:model-value="actualizar(data, { estado: $event ? 'activo' : 'bloqueado' })"
          />
        </template>
      </Column>
    </DataTable>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Un usuario con votos no se elimina: solo se bloquea. El administrador no ve contraseñas. RF-17 · RF-18.
    </p>
  </main>
</template>
