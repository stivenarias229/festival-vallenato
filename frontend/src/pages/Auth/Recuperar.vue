<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, useForm, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import FormField from "@/components/FormField.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"

const page = usePage()
const form = useForm({ email: "" })
const submit = () => form.post(page.props.urls.recuperar)
</script>

<template>
  <Head title="Recuperar contraseña" />
  <PageHeader title="Recuperar contraseña" :back-href="page.props.urls.ingresar" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <p class="text-mut">Te enviaremos un enlace si el correo está registrado.</p>
    <form class="mt-2" @submit.prevent="submit">
      <FormField label="Correo electrónico" for-id="email" :error="form.errors.email">
        <input id="email" v-model="form.email" class="field" type="email" placeholder="tu@correo.com" />
      </FormField>
      <Button type="submit" :loading="form.processing">Enviar enlace</Button>
    </form>
  </main>
</template>
