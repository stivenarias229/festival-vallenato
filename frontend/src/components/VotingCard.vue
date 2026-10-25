<script setup lang="ts">
import { Link } from "@inertiajs/vue3"

import Card from "@/components/Card.vue"
import Icon from "@/components/Icon.vue"
import StatusPill from "@/components/StatusPill.vue"

defineProps<{
  href?: string
  titulo: string
  resumen: string
  estado: string
}>()
</script>

<template>
  <component
    :is="href ? Link : 'div'"
    :href="href"
    class="block text-inherit no-underline"
  >
    <Card :interactive="Boolean(href)" :disabled="!href" class="flex items-center gap-3.5 p-4">
      <span
        class="grid size-[50px] shrink-0 place-items-center rounded-[15px] border border-gold/25 bg-linear-to-[145deg] from-gold/15 to-gold/5 text-gold"
      >
        <Icon name="vote" :size="24" />
      </span>
      <div class="min-w-0 flex-1">
        <b class="block font-serif text-[17px] leading-[1.2] font-semibold">{{ titulo }}</b>
        <small class="block text-[12.5px] text-mut">{{ resumen }}</small>
        <StatusPill :estado="estado" />
      </div>
      <Icon v-if="href" name="chevron" :size="20" class="shrink-0 text-gold" />
    </Card>
  </component>
</template>
