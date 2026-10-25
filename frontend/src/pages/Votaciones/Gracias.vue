<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import SuccessRing from "@/components/SuccessRing.vue"

defineProps<{
  votacion: { id: number }
  puede_ver_resultados: boolean
}>()

const page = usePage()
</script>

<template>
  <Head title="Voto registrado" />
  <PageHeader title="Voto registrado" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <div class="text-center">
      <SuccessRing />
      <h2 class="font-serif text-[34px] leading-[1.1] font-semibold">¡Gracias por votar!</h2>
      <p class="mt-2 mb-4 text-mut">
        Tu voto quedó guardado. ¡Que viva el Festival de la Leyenda Vallenata!
      </p>
    </div>
    <div class="card-line relative overflow-hidden rounded-[20px] border border-ln bg-linear-to-[160deg] from-s2 to-s1 p-4">
      <b class="block font-serif text-[17px] font-semibold">¿Cuándo veo los resultados?</b>
      <p class="mt-1 text-[13px] text-mut">
        Se mostrarán según lo que defina el Festival (en vivo, al cierre o solo internos).
        <i>Pendiente de validación, P-04.</i>
      </p>
    </div>
    <div class="mt-4">
      <Button v-if="puede_ver_resultados" :href="`/votaciones/${votacion.id}/resultados`">
        Ver resultados
      </Button>
      <Button :href="page.props.urls.categorias">Votar en otra categoría</Button>
      <Button variant="secondary" :href="page.props.urls.inicio">Volver al inicio</Button>
    </div>
  </main>
</template>
