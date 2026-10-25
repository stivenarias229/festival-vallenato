<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { ref } from "vue"
import { Head, useForm, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import FormField from "@/components/FormField.vue"
import SelectField from "@/components/SelectField.vue"
import Switch from "@/components/Switch.vue"
import { useServerAction } from "@/composables/useServerAction"

type Categoria = {
  id: number
  nombre: string
  descripcion: string
  icono: string
  estado: string
  edicion_id: number
}

const props = defineProps<{
  ediciones: Array<{ id: number; nombre: string; anio: number; estado: string }>
  categorias: Categoria[]
}>()

const page = usePage()
const mostrarFormulario = ref(false)
const form = useForm({
  accion: "guardar_categoria",
  id: "",
  edicion: props.ediciones[0]?.id ?? "",
  nombre: "",
  descripcion: "",
  estado: "activa",
  icono: "star",
})

const edicionForm = useForm({
  accion: "guardar_edicion",
  id: props.ediciones[0]?.id ?? "",
  nombre: props.ediciones[0]?.nombre ?? "",
  anio: props.ediciones[0]?.anio ?? 2027,
  estado: props.ediciones[0]?.estado ?? "activa",
})

const editar = (categoria: Categoria) => {
  form.id = String(categoria.id)
  form.edicion = categoria.edicion_id
  form.nombre = categoria.nombre
  form.descripcion = categoria.descripcion
  form.estado = categoria.estado
  form.icono = categoria.icono
  mostrarFormulario.value = true
}

const { processing: accionProcessing, isBusy, post } = useServerAction()

const toggle = (categoria: Categoria) => {
  post(page.props.urls.panel_categorias, { accion: "toggle_categoria", id: categoria.id }, `categoria-${categoria.id}`)
}
</script>

<template>
  <Head title="Categorías" />
  <PageHeader title="Categorías" :back-href="page.props.urls.panel" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <form class="mb-6 grid gap-3 md:grid-cols-4 md:items-end" @submit.prevent="edicionForm.post(page.props.urls.panel_categorias)">
      <FormField compact label="Edición" for-id="edicion-nombre">
        <input id="edicion-nombre" v-model="edicionForm.nombre" class="field" placeholder="Nombre de la edición" />
      </FormField>
      <FormField compact label="Año" for-id="edicion-anio">
        <input id="edicion-anio" v-model="edicionForm.anio" class="field" type="number" />
      </FormField>
      <FormField compact label="Estado" for-id="edicion-estado">
        <SelectField
          id="edicion-estado"
          v-model="edicionForm.estado"
          :options="[
            { value: 'activa', label: 'Activa' },
            { value: 'inactiva', label: 'Inactiva' },
          ]"
        />
      </FormField>
      <Button type="submit" :loading="edicionForm.processing">Guardar edición</Button>
    </form>
    <div
      v-for="categoria in categorias"
      :key="categoria.id"
      class="my-2.5 flex items-center gap-3 rounded-2xl border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-3.5 py-3"
    >
      <span class="grid size-11 place-items-center rounded-[15px] border border-gold/25 bg-gold/10 text-gold">
        <Icon :name="categoria.icono" :size="22" />
      </span>
      <div class="min-w-0 flex-1">
        <b class="block font-serif text-[17px] font-semibold">{{ categoria.nombre }}</b>
        <small class="text-[12.5px] text-mut">{{ categoria.descripcion }}</small>
      </div>
      <button type="button" class="mini" @click="editar(categoria)">
        <Icon name="edit" :size="14" />
      </button>
      <Switch
        :model-value="categoria.estado === 'activa'"
        :disabled="accionProcessing"
        :loading="isBusy(`categoria-${categoria.id}`)"
        @update:model-value="toggle(categoria)"
      />
    </div>
    <Button class="mt-4" @click="mostrarFormulario = !mostrarFormulario">
      <Icon name="plus" :size="18" />
      Nueva categoría
    </Button>
    <form v-if="mostrarFormulario" class="mt-4 grid gap-3" @submit.prevent="form.post(page.props.urls.panel_categorias)">
      <FormField compact label="Edición" for-id="categoria-edicion">
        <SelectField
          id="categoria-edicion"
          v-model="form.edicion"
          :options="ediciones.map((edicion) => ({ value: edicion.id, label: edicion.nombre }))"
        />
      </FormField>
      <FormField compact label="Nombre" for-id="categoria-nombre">
        <input id="categoria-nombre" v-model="form.nombre" class="field" placeholder="Ej. Acordeón" />
      </FormField>
      <FormField compact label="Descripción" for-id="categoria-descripcion">
        <input id="categoria-descripcion" v-model="form.descripcion" class="field" placeholder="Breve descripción" />
      </FormField>
      <FormField compact label="Icono" for-id="categoria-icono">
        <SelectField
          id="categoria-icono"
          v-model="form.icono"
          :options="[
            { value: 'acc', label: 'Acordeón' },
            { value: 'music', label: 'Música' },
            { value: 'mic', label: 'Micrófono' },
            { value: 'star', label: 'Estrella' },
          ]"
        />
      </FormField>
      <Button type="submit" :loading="form.processing">Guardar categoría</Button>
    </form>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Datos de ejemplo pendientes de validación.
    </p>
  </main>
</template>
