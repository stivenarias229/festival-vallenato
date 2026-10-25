<script setup lang="ts">
import { Link } from "@inertiajs/vue3"

import Card from "@/components/Card.vue"
import Icon from "@/components/Icon.vue"

defineProps<{
  href: string
  icono: string
  nombre: string
  descripcion: string
}>()
</script>

<template>
  <Link :href="href" class="block text-inherit no-underline">
    <Card interactive class="flex items-center gap-3.5 p-4">
      <span
        class="grid size-[50px] shrink-0 place-items-center rounded-[15px] border border-gold/25 bg-linear-to-[145deg] from-gold/15 to-gold/5 text-gold"
      >
        <Icon :name="icono" :size="24" />
      </span>
      <div class="min-w-0 flex-1">
        <b class="block font-serif text-[17px] leading-[1.2] font-semibold">{{ nombre }}</b>
        <small class="block text-[12.5px] text-mut">{{ descripcion }}</small>
      </div>
      <Icon name="chevron" :size="20" class="shrink-0 text-gold" />
    </Card>
  </Link>
</template>
