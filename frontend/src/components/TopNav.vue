<script setup lang="ts">
import { computed } from "vue"
import { Link, usePage } from "@inertiajs/vue3"

import Icon from "@/components/Icon.vue"

const page = usePage()
const urls = computed(() => page.props.urls)
const user = computed(() => page.props.auth?.user)
const path = computed(() => page.url.split("?")[0])

const items = computed(() => [
  { href: urls.value.inicio, label: "Inicio", match: ["/"] },
  { href: urls.value.categorias, label: "Votar", match: ["/categorias", "/votaciones"] },
  {
    href: user.value ? urls.value.salir : urls.value.ingresar,
    label: user.value ? "Cerrar sesión" : "Cuenta",
    match: ["/ingresar", "/registro"],
  },
])

const isOn = (match: string[]) => {
  if (match.includes("/") && path.value === "/") return true
  return match.some((item) => item !== "/" && (path.value === item || path.value.startsWith(`${item}/`)))
}
</script>

<template>
  <nav class="hidden items-center gap-2 lg:flex" aria-label="Navegación principal">
    <Link
      v-for="item in items"
      :key="item.label"
      :href="item.href"
      class="inline-flex min-h-11 items-center rounded-full px-4 text-sm font-bold no-underline"
      :class="isOn(item.match) ? 'bg-gold/15 text-gold-2' : 'text-mut hover:text-ivory'"
    >
      {{ item.label }}
    </Link>
    <Link
      v-if="user?.rol === 'administrador'"
      :href="urls.panel"
      class="inline-flex min-h-11 items-center gap-2 rounded-full border border-gold/40 px-4 text-sm font-bold text-gold no-underline"
    >
      <Icon name="grid" :size="18" />
      Panel
    </Link>
  </nav>
</template>
