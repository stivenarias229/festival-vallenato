<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { computed } from "vue"
import { Head, usePage } from "@inertiajs/vue3"

import AccordionHero from "@/components/AccordionHero.vue"
import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"

const page = usePage()
const sesionActiva = computed(() => Boolean(page.props.auth?.user))
const pasos = [
  "Crea tu cuenta o inicia sesión",
  "Escoge una categoría",
  "Elige tu opción favorita",
  "Confirma tu voto",
]
</script>

<template>
  <Head title="Inicio" />
  <PageHeader title="Leyenda 2027" />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8 lg:grid lg:grid-cols-2 lg:items-center lg:gap-10">
    <section>
      <p class="text-[10px] font-extrabold tracking-[0.18em] text-gold uppercase">
        Festival de la Leyenda Vallenata
      </p>
      <h2 class="mt-2.5 font-serif text-[47px] leading-[1.02] font-semibold tracking-[-0.02em]">
        Tu voto,<br />
        <em class="font-medium text-gold-2 italic">tu leyenda</em>
      </h2>
      <p class="mt-3 mb-2 max-w-[34ch] text-mut">
        Elige a tus favoritos desde el celular, de forma simple y segura.
      </p>
      <AccordionHero class="lg:hidden" />
      <Button :href="page.props.urls.categorias">
        Explorar votaciones
        <Icon name="chevron" :size="20" />
      </Button>
      <Button v-if="!sesionActiva" variant="secondary" :href="page.props.urls.registro">
        Crear mi cuenta
      </Button>
    </section>
    <section class="lg:block">
      <AccordionHero class="hidden lg:block" />
      <h3 class="mt-6 mb-2 font-serif text-xl font-semibold">Así se vota</h3>
      <div class="card-line relative overflow-hidden rounded-[20px] border border-ln bg-linear-to-[160deg] from-s2 to-s1 p-4">
        <div
          v-for="(paso, index) in pasos"
          :key="paso"
          class="flex items-center gap-3.5 border-b border-ln py-2.5 last:border-0"
        >
          <b class="font-serif text-2xl font-medium text-gold">0{{ index + 1 }}</b>
          <span>{{ paso }}</span>
        </div>
      </div>
      <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
        Datos de ejemplo: categorías, votaciones, opciones y usuarios son ilustrativos y están
        <b class="text-gold-2">pendientes de validación</b> con el cliente.
      </p>
    </section>
  </main>
</template>
