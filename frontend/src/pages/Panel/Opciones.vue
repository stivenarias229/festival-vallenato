<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { nextTick, ref } from "vue"
import { Head, router, useForm, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import FormField from "@/components/FormField.vue"
import SelectField from "@/components/SelectField.vue"
import { useServerAction } from "@/composables/useServerAction"

type Opcion = { id: number; nombre: string; descripcion: string; orden: number }

const props = defineProps<{
  votacion: { id: number; titulo: string }
  opciones: Opcion[]
  votaciones: Array<{ id: number; titulo: string }>
}>()

const page = usePage()
const mostrar = ref(false)
const formulario = ref<HTMLElement | null>(null)
const form = useForm({
  accion: "guardar",
  id: "",
  nombre: "",
  descripcion: "",
  orden: props.opciones.length + 1,
  imagen: null as File | null,
})

const cambiarVotacion = (id: string | number | null) => {
  if (id == null) return
  router.get(`/panel/votaciones/${id}/opciones`)
}

const mostrarFormulario = async () => {
  mostrar.value = true
  await nextTick()
  formulario.value?.scrollIntoView({ behavior: "smooth", block: "center" })
}

const nueva = () => {
  form.id = ""
  form.nombre = ""
  form.descripcion = ""
  form.orden = props.opciones.length + 1
  form.imagen = null
  void mostrarFormulario()
}

const editar = (opcion: Opcion) => {
  form.id = String(opcion.id)
  form.nombre = opcion.nombre
  form.descripcion = opcion.descripcion
  form.orden = opcion.orden
  form.imagen = null
  void mostrarFormulario()
}

const { processing: accionProcessing, isBusy, post } = useServerAction()

const mover = (id: number, accion: "subir" | "bajar") => {
  post(`/panel/votaciones/${props.votacion.id}/opciones`, { accion, id }, `${accion}-${id}`)
}
</script>

<template>
  <Head title="Opciones" />
  <PageHeader title="Opciones" :back-href="page.props.urls.panel_votaciones" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <FormField compact label="Votación" for-id="opciones-votacion">
      <SelectField
        id="opciones-votacion"
        :model-value="votacion.id"
        :options="votaciones.map((item) => ({ value: item.id, label: item.titulo }))"
        @update:model-value="cambiarVotacion"
      />
    </FormField>
    <div
      v-for="(opcion, indice) in opciones"
      :key="opcion.id"
      class="my-2.5 flex items-center gap-3 rounded-2xl border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-3.5 py-3"
    >
      <div class="grid size-[46px] place-items-center rounded-2xl bg-linear-to-br from-gold-2 to-ember font-serif text-xl text-ink">
        {{ opcion.nombre.slice(-1) }}
      </div>
      <div class="min-w-0 flex-1">
        <b class="block font-serif text-[17px] font-semibold">{{ opcion.nombre }}</b>
        <small class="text-mut">{{ opcion.descripcion }}</small>
      </div>
      <Button
        size="mini"
        variant="secondary"
        aria-label="Subir"
        :loading="isBusy(`subir-${opcion.id}`)"
        :disabled="accionProcessing || indice === 0"
        @click="mover(opcion.id, 'subir')"
      >
        <Icon name="up" :size="14" />
      </Button>
      <Button
        size="mini"
        variant="secondary"
        aria-label="Bajar"
        :loading="isBusy(`bajar-${opcion.id}`)"
        :disabled="accionProcessing || indice === opciones.length - 1"
        @click="mover(opcion.id, 'bajar')"
      >
        <Icon name="down" :size="14" />
      </Button>
      <button type="button" class="mini" aria-label="Editar" @click="editar(opcion)">
        <Icon name="edit" :size="14" />
      </button>
    </div>
    <Button class="mt-4" @click="nueva">
      <Icon name="plus" :size="18" />
      Nueva opción
    </Button>
    <form
      v-if="mostrar"
      ref="formulario"
      class="mt-4 grid gap-3"
      @submit.prevent="form.post(`/panel/votaciones/${votacion.id}/opciones`)"
    >
      <p class="font-serif text-lg font-semibold text-gold-2">
        {{ form.id ? "Editar opción" : "Nueva opción" }}
      </p>
      <FormField compact label="Nombre" for-id="opcion-nombre">
        <input id="opcion-nombre" v-model="form.nombre" class="field" placeholder="Nombre de la opción" />
      </FormField>
      <FormField compact label="Descripción" for-id="opcion-descripcion">
        <input id="opcion-descripcion" v-model="form.descripcion" class="field" placeholder="Breve descripción" />
      </FormField>
      <FormField compact label="Orden" for-id="opcion-orden">
        <input id="opcion-orden" v-model.number="form.orden" class="field" type="number" min="0" />
      </FormField>
      <FormField compact label="Imagen" for-id="opcion-imagen">
        <input
          id="opcion-imagen"
          class="field"
          type="file"
          accept="image/*"
          @change="form.imagen = ($event.target as HTMLInputElement).files?.[0] ?? null"
        />
      </FormField>
      <Button type="submit" :loading="form.processing">Guardar opción</Button>
    </form>
  </main>
</template>
