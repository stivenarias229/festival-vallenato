<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { Head, router, usePage } from "@inertiajs/vue3"

import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import Pagination from "@/components/Pagination.vue"
import FormField from "@/components/FormField.vue"
import SelectField from "@/components/SelectField.vue"
import Switch from "@/components/Switch.vue"
import UserFilters from "@/components/UserFilters.vue"
import { useServerAction } from "@/composables/useServerAction"

const rolesUsuario = [
  { value: "votante", label: "Votante" },
  { value: "administrador", label: "Administrador" },
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
  filtro: string
  q: string
  paginacion: {
    number: number
    num_pages: number
    count: number
    has_next: boolean
    has_previous: boolean
    next_page: number | null
    previous_page: number | null
  }
}>()

const page = usePage()
const yo = page.props.auth.user

const { processing, isBusy, post } = useServerAction()

const consultar = (params: Record<string, string | number>) => {
  router.get(page.props.urls.panel_usuarios, params, { preserveState: true, replace: true })
}

const actualizar = (usuario: Usuario, cambios: Partial<Usuario>) => {
  if (yo && usuario.id === yo.id) return
  post(
    page.props.urls.panel_usuarios,
    {
      id: usuario.id,
      rol: cambios.rol ?? usuario.rol,
      estado: cambios.estado ?? usuario.estado,
    },
    `usuario-${usuario.id}`,
  )
}

const links = Array.from({ length: props.paginacion.num_pages }, (_, index) => ({
  url: `${page.props.urls.panel_usuarios}?filtro=${props.filtro}&q=${props.q}&page=${index + 1}`,
  label: String(index + 1),
  active: props.paginacion.number === index + 1,
}))
</script>

<template>
  <Head title="Usuarios" />
  <PageHeader title="Usuarios" :back-href="page.props.urls.panel" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <UserFilters
      :q="q"
      :filtro="filtro"
      @buscar="(valor) => consultar({ q: valor, filtro })"
      @filtrar="(valor) => consultar({ q, filtro: valor })"
    />
    <div class="mt-4 hidden overflow-x-auto lg:block">
      <table class="w-full text-left text-sm">
        <thead class="text-mut">
          <tr>
            <th class="p-3">Nombre</th>
            <th class="p-3">Correo</th>
            <th class="p-3">Rol</th>
            <th class="p-3">Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in usuarios" :key="usuario.id" class="border-t border-ln">
            <td class="p-3 font-serif">{{ usuario.nombre }}</td>
            <td class="p-3 text-mut">{{ usuario.email }}</td>
            <td class="p-3">
              <SelectField
                compact
                :model-value="usuario.rol"
                :options="rolesUsuario"
                :disabled="yo?.id === usuario.id || processing"
                @update:model-value="(rol) => actualizar(usuario, { rol: String(rol) })"
              />
            </td>
            <td class="p-3">
              <Switch
                :model-value="usuario.estado === 'activo'"
                :disabled="yo?.id === usuario.id || processing"
                :loading="isBusy(`usuario-${usuario.id}`)"
                @update:model-value="actualizar(usuario, { estado: $event ? 'activo' : 'bloqueado' })"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="lg:hidden">
      <div
        v-for="usuario in usuarios"
        :key="usuario.id"
        class="my-2.5 flex items-center gap-3 rounded-2xl border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-3.5 py-3"
      >
        <div class="grid size-11 place-items-center rounded-full bg-linear-to-br from-gold-2 to-ember font-serif text-lg text-ink">
          {{ usuario.nombre.slice(0, 1) }}
        </div>
        <div class="min-w-0 flex-1">
          <b class="block font-serif text-[17px] font-semibold">{{ usuario.nombre }}</b>
          <small class="text-mut">{{ usuario.email }}</small>
          <FormField compact class="mt-2" label="Rol" :for-id="`usuario-rol-${usuario.id}`">
            <SelectField
              compact
              :id="`usuario-rol-${usuario.id}`"
              :model-value="usuario.rol"
              :options="rolesUsuario"
              :disabled="yo?.id === usuario.id || processing"
              @update:model-value="(rol) => actualizar(usuario, { rol: String(rol) })"
            />
          </FormField>
        </div>
        <div class="w-16 text-center text-[11px] text-mut">
          <Switch
            :model-value="usuario.estado === 'activo'"
            :disabled="yo?.id === usuario.id || processing"
            :loading="isBusy(`usuario-${usuario.id}`)"
            @update:model-value="actualizar(usuario, { estado: $event ? 'activo' : 'bloqueado' })"
          />
          <span>{{ usuario.estado === "activo" ? "Activo" : "Bloqueado" }}</span>
        </div>
      </div>
    </div>
    <Pagination :links="links" />
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Un usuario con votos no se elimina: solo se bloquea. El administrador no ve contraseñas. RF-17 · RF-18.
    </p>
  </main>
</template>
