<script setup lang="ts">
import { computed } from "vue"
import { Link, usePage } from "@inertiajs/vue3"

import Icon from "@/components/Icon.vue"

const props = defineProps<{
  admin?: boolean
}>()

const page = usePage()
const urls = computed(() => page.props.urls)
const user = computed(() => page.props.auth?.user)
const path = computed(() => page.url.split("?")[0])

const items = computed(() => {
  if (props.admin) {
    return [
      { href: urls.value.panel, icon: "home", label: "Panel", match: ["/panel"] },
      { href: urls.value.panel_categorias, icon: "grid", label: "Categ.", match: ["/panel/categorias"] },
      { href: urls.value.panel_votaciones, icon: "vote", label: "Votac.", match: ["/panel/votaciones"] },
      { href: urls.value.panel_usuarios, icon: "users", label: "Usuarios", match: ["/panel/usuarios"] },
      { href: urls.value.panel_resultados, icon: "chart", label: "Result.", match: ["/panel/resultados"] },
    ]
  }
  return [
    { href: urls.value.inicio, icon: "home", label: "Inicio", match: ["/"] },
    { href: urls.value.categorias, icon: "ticket", label: "Votar", match: ["/categorias"] },
    { href: urls.value.categorias, icon: "vote", label: "Votaciones", match: ["/votaciones"] },
    {
      href: user.value ? urls.value.salir : urls.value.ingresar,
      icon: "user",
      label: user.value ? "Salir" : "Cuenta",
      match: ["/ingresar", "/registro", "/recuperar"],
    },
  ]
})

const isOn = (match: string[]) => {
  if (match.includes("/") && path.value === "/") return true
  return match.some((item) => item !== "/" && (path.value === item || path.value.startsWith(`${item}/`)))
}
</script>

<template>
  <nav
    class="sticky bottom-[calc(12px+env(safe-area-inset-bottom,0px))] z-10 mx-3.5 mb-3.5 flex rounded-3xl border border-ln bg-[#1a1424d9] p-2 shadow-[0_14px_40px_#000a] backdrop-blur-2xl"
    aria-label="Navegación principal"
  >
    <Link
      v-for="item in items"
      :key="item.label"
      :href="item.href"
      class="flex min-h-11 flex-1 flex-col items-center justify-center gap-0.5 rounded-2xl py-2 text-[10px] font-bold no-underline"
      :class="isOn(item.match) ? 'bg-gold/12 text-gold-2' : 'text-mut'"
    >
      <Icon :name="item.icon" :size="22" />
      {{ item.label }}
    </Link>
  </nav>
</template>
