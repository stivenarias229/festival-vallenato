<script setup lang="ts">
import { computed } from "vue"
import { Link, usePage } from "@inertiajs/vue3"

import Icon from "@/components/Icon.vue"

const page = usePage()
const urls = computed(() => page.props.urls)
const path = computed(() => page.url.split("?")[0])

const items = computed(() => [
  { href: urls.value.panel, icon: "home", label: "Panel", match: ["/panel"] },
  { href: urls.value.panel_categorias, icon: "grid", label: "Categorías", match: ["/panel/categorias"] },
  { href: urls.value.panel_votaciones, icon: "vote", label: "Votaciones", match: ["/panel/votaciones"] },
  { href: urls.value.panel_usuarios, icon: "users", label: "Usuarios", match: ["/panel/usuarios"] },
  { href: urls.value.panel_resultados, icon: "chart", label: "Resultados", match: ["/panel/resultados"] },
  { href: urls.value.panel_actividad, icon: "edit", label: "Actividad", match: ["/panel/actividad"] },
])

const isOn = (href: string, match: string[]) => {
  if (href === urls.value.panel) return path.value === "/panel"
  return match.some((item) => path.value === item || path.value.startsWith(`${item}/`))
}
</script>

<template>
  <aside
    class="hidden w-60 shrink-0 border-r border-ln bg-s1/80 p-4 lg:block"
    aria-label="Navegación de administración"
  >
    <p class="mb-4 px-2 font-serif text-lg font-semibold text-gold">Administración</p>
    <nav class="flex flex-col gap-1">
      <Link
        v-for="item in items"
        :key="item.label"
        :href="item.href"
        class="flex min-h-11 items-center gap-3 rounded-2xl px-3 text-sm font-bold no-underline"
        :class="isOn(item.href, item.match) ? 'bg-gold/15 text-gold-2' : 'text-mut hover:text-ivory'"
      >
        <Icon :name="item.icon" :size="20" />
        {{ item.label }}
      </Link>
    </nav>
  </aside>
</template>
