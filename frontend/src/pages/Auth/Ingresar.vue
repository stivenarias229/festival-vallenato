<script lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"

export default { layout: AppLayout }
</script>

<script setup lang="ts">
import { Head, Link, useForm, usePage } from "@inertiajs/vue3"

import Button from "@/components/Button.vue"
import FormField from "@/components/FormField.vue"
import MochilaBand from "@/components/MochilaBand.vue"
import PageHeader from "@/components/PageHeader.vue"

const props = defineProps<{
  errors?: Record<string, string>
  next?: string
}>()

const page = usePage()
const form = useForm({
  email: "",
  password: "",
  next: props.next ?? "",
})

const firstError = (key: "email" | "password") => {
  const value = form.errors[key] || props.errors?.[key]
  return Array.isArray(value) ? value[0] : value
}

const submit = () => form.post(page.props.urls.ingresar)
</script>

<template>
  <Head title="Iniciar sesión" />
  <PageHeader title="Iniciar sesión" :back-href="page.props.urls.inicio" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <form @submit.prevent="submit">
      <FormField label="Correo electrónico" for-id="email" :error="firstError('email')">
        <input id="email" v-model="form.email" name="email" class="field" type="email" placeholder="tu@correo.com" autocomplete="email" />
      </FormField>
      <FormField label="Contraseña" for-id="password" :error="firstError('password')">
        <input id="password" v-model="form.password" name="password" class="field" type="password" placeholder="••••••••" autocomplete="current-password" />
      </FormField>
      <Button type="submit" :loading="form.processing">Ingresar</Button>
    </form>
    <p class="mt-3 text-center">
      <Link :href="page.props.urls.recuperar" class="text-[13px] font-extrabold text-gold no-underline">
        ¿Olvidaste tu contraseña?
      </Link>
    </p>
    <Button variant="secondary" :href="page.props.urls.registro">Crear cuenta nueva</Button>
  </main>
</template>
