<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default {
  layout: AppLayout,
}
</script>

<script setup lang="ts">
import { Head } from "@inertiajs/vue3"

defineProps<{
  app_name: string
}>()
</script>

<template>
  <Head title="Inicio" />
  <main class="mx-auto flex max-w-3xl flex-col gap-6 px-6 py-16">
    <div class="space-y-3">
      <p class="text-sm font-medium text-neutral-500">Django + Inertia</p>
      <h1 class="text-4xl font-semibold tracking-tight text-neutral-950">{{ app_name }}</h1>
      <p class="text-lg text-neutral-500">
        Vue 3 y Tailwind CSS, en la misma aplicación.
      </p>
    </div>
    <div>
      <button
        type="button"
        class="inline-flex h-9 items-center rounded-md bg-neutral-900 px-4 text-sm font-medium text-white"
      >
        Listo para desarrollar
      </button>
    </div>
  </main>
</template>
