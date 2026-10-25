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

defineProps<{
  errors?: Record<string, string | string[]>
}>()

const page = usePage()
const form = useForm({
  nombre: "",
  email: "",
  password: "",
  acepto_tratamiento: false,
})

const firstError = (key: "nombre" | "email" | "password" | "acepto_tratamiento") => {
  const value = form.errors[key]
  return Array.isArray(value) ? value[0] : value
}

const submit = () => form.post(page.props.urls.registro)
</script>

<template>
  <Head title="Crear cuenta" />
  <PageHeader title="Crear cuenta" :back-href="page.props.urls.inicio" />
  <MochilaBand />
  <main class="mx-auto w-full max-w-md flex-1 px-[18px] pt-4 pb-8">
    <p class="text-mut">Solo pedimos los datos mínimos para que puedas votar.</p>
    <form class="mt-2" @submit.prevent="submit">
      <FormField label="Nombre completo" for-id="nombre" :error="firstError('nombre')">
        <input id="nombre" v-model="form.nombre" class="field" type="text" placeholder="Tu nombre" autocomplete="name" />
      </FormField>
      <FormField label="Correo electrónico" for-id="email" :error="firstError('email')">
        <input id="email" v-model="form.email" class="field" type="email" placeholder="tu@correo.com" autocomplete="email" />
      </FormField>
      <FormField label="Contraseña" for-id="password" :error="firstError('password')">
        <input
          id="password"
          v-model="form.password"
          class="field"
          type="password"
          placeholder="Mínimo 8 caracteres"
          autocomplete="new-password"
        />
      </FormField>
      <label class="my-3.5 flex gap-2.5 text-[13px] text-mut">
        <input v-model="form.acepto_tratamiento" type="checkbox" class="mt-0.5 size-[18px] shrink-0 accent-gold" />
        <span>Autorizo el tratamiento de mis datos personales (Ley 1581 de 2012).</span>
      </label>
      <p v-if="firstError('acepto_tratamiento')" class="text-[13px] text-ember" role="alert">
        {{ firstError("acepto_tratamiento") }}
      </p>
      <Button type="submit" :loading="form.processing">Crear cuenta</Button>
    </form>
    <p class="mt-4 rounded-[14px] border border-dashed border-gold/35 bg-gold/5 px-3 py-2.5 text-[12.5px] text-mut">
      RF-01 · RF-11. Datos solicitados y método de identificación
      <b class="text-gold-2">pendientes de validación</b> (P-01, P-07).
    </p>
  </main>
</template>
