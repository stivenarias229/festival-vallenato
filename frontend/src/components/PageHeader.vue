<script setup lang="ts">
import { Link } from "@inertiajs/vue3"

import Icon from "@/components/Icon.vue"

defineProps<{
  title: string
  backHref?: string
  admin?: boolean
}>()
</script>

<template>
  <header
    class="sticky top-0 z-5 flex items-center gap-3 bg-linear-to-b from-bg from-65% to-transparent px-[18px] pt-4 pb-3"
  >
    <Link
      v-if="backHref"
      :href="backHref"
      class="grid size-[44px] shrink-0 place-items-center rounded-full border border-ln bg-white/5 text-gold"
      aria-label="Volver"
    >
      <Icon name="back" :size="20" />
    </Link>
    <span
      v-else
      class="grid size-[38px] shrink-0 place-items-center rounded-xl bg-linear-to-br from-gold-2 to-gold text-ink"
      aria-hidden="true"
    >
      <Icon name="accordion" :size="20" />
    </span>
    <h1 class="flex-1 font-serif text-[22px] leading-[1.1] font-semibold">{{ title }}</h1>
    <span
      v-if="admin"
      class="rounded-full border border-gold px-2.5 py-1 text-[10px] font-extrabold tracking-[0.14em] text-gold"
    >
      ADMIN
    </span>
    <slot name="actions" />
  </header>
</template>
