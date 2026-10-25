<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, useForm } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import FormField from "@/components/FormField.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"

const form = useForm({ password: "" })
const submit = () => form.post(window.location.pathname)
</script>

<template>
  <Head title="Nueva contraseña" />
  <PageHeader title="Nueva contraseña" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <form @submit.prevent="submit">
      <FormField label="Nueva contraseña" for-id="password" :error="form.errors.password">
        <input id="password" v-model="form.password" class="field" type="password" autocomplete="new-password" />
      </FormField>
      <Button type="submit" :loading="form.processing">Guardar contraseña</Button>
    </form>
  </main>
</template>
