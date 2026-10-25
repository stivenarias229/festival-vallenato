<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { ref } from "vue"
import { Head, Link, useForm, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import DateTimeField from "@/components/DateTimeField.vue"
import FormField from "@/components/FormField.vue"
import SelectField from "@/components/SelectField.vue"
import StatusPill from "@/components/StatusPill.vue"
import { useServerAction } from "@/composables/useServerAction"

type Votacion = {
  id: number
  titulo: string
  categoria_id: number
  fecha_inicio: string
  fecha_fin: string
  estado: string
  estado_efectivo: string
  reglas: string
  visibilidad_resultados: string
  limite_votos_por_usuario: number
  resumen_fecha: string
}

const props = defineProps<{
  categorias: Array<{ id: number; nombre: string }>
  votaciones: Votacion[]
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

const cambiarEstado = (id: number, accion: "abrir" | "cerrar") => {
  post(page.props.urls.panel_votaciones, { accion, id }, `estado-${id}`)
}
</script>

<template>
  <Head title="Votaciones" />
  <PageHeader title="Votaciones" :back-href="page.props.urls.panel" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <div class="hidden overflow-x-auto lg:block">
      <table class="w-full text-left text-sm">
        <thead class="text-mut">
          <tr>
            <th class="p-3">Título</th>
            <th class="p-3">Fechas</th>
            <th class="p-3">Estado</th>
            <th class="p-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="votacion in votaciones" :key="votacion.id" class="border-t border-ln">
            <td class="p-3 font-serif text-base">{{ votacion.titulo }}</td>
            <td class="p-3 text-mut">{{ votacion.resumen_fecha }}</td>
            <td class="p-3"><StatusPill :estado="votacion.estado_efectivo" /></td>
            <td class="flex flex-wrap gap-2 p-3">
              <Link class="mini" :href="`/panel/votaciones/${votacion.id}/opciones`">Opciones</Link>
              <button type="button" class="mini" @click="editar(votacion)">Editar</button>
              <Button
                size="mini"
                variant="secondary"
                :loading="isBusy(`estado-${votacion.id}`)"
                :disabled="accionProcessing"
                @click="cambiarEstado(votacion.id, votacion.estado === 'abierta' ? 'cerrar' : 'abrir')"
              >
                {{ votacion.estado === "abierta" ? "Cerrar" : "Abrir" }}
              </Button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="lg:hidden">
      <div
        v-for="votacion in votaciones"
        :key="votacion.id"
        class="my-2.5 flex flex-col gap-2 rounded-2xl border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-3.5 py-3"
      >
        <div>
          <b class="block font-serif text-[17px] font-semibold">{{ votacion.titulo }}</b>
          <small class="text-mut">{{ votacion.resumen_fecha }}</small>
          <StatusPill :estado="votacion.estado_efectivo" />
        </div>
        <div class="flex flex-wrap gap-2">
          <Link class="mini" :href="`/panel/votaciones/${votacion.id}/opciones`">Opciones</Link>
          <button type="button" class="mini" @click="editar(votacion)">Editar</button>
          <Button
            size="mini"
            variant="secondary"
            :loading="isBusy(`estado-${votacion.id}`)"
            :disabled="accionProcessing"
            @click="cambiarEstado(votacion.id, votacion.estado === 'abierta' ? 'cerrar' : 'abrir')"
          >
            {{ votacion.estado === "abierta" ? "Cerrar" : "Abrir" }}
          </Button>
        </div>
      </div>
    </div>
    <Button class="mt-4" @click="mostrar = !mostrar">
      <Icon name="plus" :size="18" />
      Nueva votación
    </Button>
    <form v-if="mostrar" class="mt-4 grid gap-3" @submit.prevent="form.post(page.props.urls.panel_votaciones)">
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
