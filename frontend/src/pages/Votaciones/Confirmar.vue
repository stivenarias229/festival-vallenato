<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { ref } from "vue"
import { Head, useForm } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import StepIndicator from "@/components/StepIndicator.vue"
import Ticket from "@/components/Ticket.vue"

const props = defineProps<{
  votacion: { id: number; titulo: string }
  opcion: { id: number; nombre: string; descripcion: string }
}>()

const entendido = ref(false)
const form = useForm({
  opcion_id: props.opcion.id,
  confirmado: "1",
})

const confirmar = () => {
  if (!entendido.value) return
  form.post(`/votaciones/${props.votacion.id}/votar`)
}
</script>

<template>
  <Head title="Confirma tu voto" />
  <PageHeader title="Confirma tu voto" :back-href="`/votaciones/${votacion.id}/opciones`" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <StepIndicator :current="3" />
    <Ticket :votacion="votacion.titulo" :opcion="opcion.nombre" :descripcion="opcion.descripcion" />
    <label class="my-3.5 flex gap-2.5 text-[13px] text-mut">
      <input v-model="entendido" type="checkbox" class="mt-0.5 size-[18px] shrink-0 accent-gold" />
      <span>Entiendo que una vez confirmado no podré modificarlo.</span>
    </label>
    <Button :disabled="!entendido" :loading="form.processing" @click="confirmar">Confirmar mi voto</Button>
    <Button variant="secondary" :href="`/votaciones/${votacion.id}/opciones`">Cambiar mi elección</Button>
  </main>
</template>
