<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { Head, router, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import FormField from "@/components/FormField.vue"
import ResultBar from "@/components/ResultBar.vue"
import SelectField from "@/components/SelectField.vue"

const props = defineProps<{
  votaciones: Array<{ id: number; titulo: string }>
  votacion: { id: number; titulo: string } | null
  resultados: { total: number; opciones: Array<{ nombre: string; porcentaje: number; votos: number }> }
}>()

const page = usePage()

const cambiar = (id: string | number | null) => {
  if (id == null) return
  router.get(page.props.urls.panel_resultados, { votacion: id })
}
</script>

<template>
  <Head title="Resultados" />
  <PageHeader title="Resultados" :back-href="page.props.urls.panel" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <FormField compact label="Votación" for-id="resultados-votacion">
      <SelectField
        id="resultados-votacion"
        :model-value="votacion?.id ?? null"
        :options="votaciones.map((item) => ({ value: item.id, label: item.titulo }))"
        @update:model-value="cambiar"
      />
    </FormField>
    <div class="mt-6">
      <ResultBar
        v-for="opcion in resultados.opciones"
        :key="opcion.nombre"
        :nombre="opcion.nombre"
        :porcentaje="opcion.porcentaje"
        :votos="opcion.votos"
      />
    </div>
    <Button
      v-if="votacion"
      class="mt-4"
      :href="`/panel/resultados/${votacion.id}/csv`"
    >
      <Icon name="download" :size="18" />
      Exportar resultados
    </Button>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Solo conteos y porcentajes. Qué se publica al público depende de P-04.
    </p>
  </main>
</template>
