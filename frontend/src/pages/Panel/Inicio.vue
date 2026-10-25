<script lang="ts">
import AdminLayout from "@/layouts/AdminLayout.vue"

export default { layout: AdminLayout }
</script>

<script setup lang="ts">
import { Head, Link, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import Icon from "@/components/Icon.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"
import StatCard from "@/components/StatCard.vue"

defineProps<{
  stats: { votos: number; votaciones_abiertas: number; usuarios: number }
  actividad: Array<{ id: number; accion: string; detalle: string; fecha_hora: string; usuario: string }>
}>()

const page = usePage()
const atajos = [
  { href: page.props.urls.panel_categorias, icon: "grid", label: "Categorías" },
  { href: page.props.urls.panel_votaciones, icon: "vote", label: "Votaciones" },
  { href: page.props.urls.panel_usuarios, icon: "users", label: "Usuarios" },
  { href: page.props.urls.panel_resultados, icon: "chart", label: "Resultados" },
  { href: page.props.urls.panel_actividad, icon: "edit", label: "Actividad" },
]
</script>

<template>
  <Head title="Panel del Festival" />
  <PageHeader title="Panel del Festival" admin />
  <MochilaBand />
  <main class="flex-1 px-[18px] pt-4 pb-8">
    <div class="grid grid-cols-3 gap-2.5">
      <StatCard :valor="stats.votos.toLocaleString('es-CO')" etiqueta="votos" />
      <StatCard :valor="stats.votaciones_abiertas" etiqueta="votaciones abiertas" />
      <StatCard :valor="stats.usuarios" etiqueta="usuarios" />
    </div>
    <div class="mt-4 grid grid-cols-2 gap-3">
      <Link
        v-for="atajo in atajos"
        :key="atajo.label"
        :href="atajo.href"
        class="card-line relative flex flex-col items-start gap-3 rounded-[20px] border border-ln bg-linear-to-[160deg] from-s2 to-s1 p-4 text-inherit no-underline last:col-span-2"
      >
        <span class="grid size-[50px] place-items-center rounded-[15px] border border-gold/25 bg-gold/10 text-gold">
          <Icon :name="atajo.icon" :size="24" />
        </span>
        <b class="font-serif text-[17px] font-semibold">{{ atajo.label }}</b>
      </Link>
    </div>
    <h3 class="mt-6 mb-2 font-serif text-xl font-semibold">Actividad reciente</h3>
    <div
      v-for="item in actividad"
      :key="item.id"
      class="my-2.5 flex items-center rounded-2xl border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-3.5 py-3"
    >
      <div>
        <b class="block font-serif text-[17px] font-semibold">{{ item.accion }}</b>
        <small class="text-[12.5px] text-mut">{{ item.usuario }} · {{ item.detalle }}</small>
      </div>
    </div>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      Registro de actividad: RF-16.
    </p>
    <Button class="mt-3" variant="secondary" :href="page.props.urls.salir">Cerrar sesión</Button>
  </main>
</template>
