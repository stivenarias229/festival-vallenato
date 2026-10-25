<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"

const page = usePage()
</script>

<template>
  <Head title="Revisa tu correo" />
  <PageHeader title="Revisa tu correo" :back-href="page.props.urls.ingresar" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <p class="text-mut">
      Te enviamos un enlace de un solo uso para verificar tu cuenta. En desarrollo el correo llega a Mailtrap.
    </p>
    <Button class="mt-4" :href="page.props.urls.ingresar">Ir a iniciar sesión</Button>
  </main>
</template>
