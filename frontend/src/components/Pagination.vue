<script setup lang="ts">
import { Link } from "@inertiajs/vue3"

export interface PageLink {
  url: string | null
  label: string
  active: boolean
}

defineProps<{
  links: PageLink[]
}>()
</script>

<template>
  <nav v-if="links.length > 3" class="mt-4 flex flex-wrap justify-center gap-1" aria-label="Paginación">
    <Link
      v-for="link in links"
      :key="`${link.label}-${link.url}`"
      :href="link.url ?? '#'"
      class="min-h-11 min-w-11 rounded-[10px] border px-3 py-2 text-xs font-bold no-underline"
      :class="
        link.active
          ? 'border-gold bg-gold text-ink'
          : 'border-ln bg-white/5 text-ivory'
      "
      :tabindex="link.url ? 0 : -1"
      v-html="link.label"
    />
  </nav>
</template>
