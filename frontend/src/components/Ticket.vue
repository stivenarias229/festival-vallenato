<script setup lang="ts">
defineProps<{
  votacion: string
  opcion: string
  descripcion: string
  pie?: string
}>()
</script>

<template>
  <article class="my-2.5 mb-4 rounded-[22px] border border-gold/35 bg-linear-to-[160deg] from-[#2a2036] to-[#17121f]">
    <div class="px-5 py-[22px]">
      <small class="text-mut">Tu voto en «{{ votacion }}»</small>
      <b class="mt-1.5 block font-serif text-[28px] leading-[1.1] font-semibold">{{ opcion }}</b>
      <small class="text-mut">{{ descripcion }}</small>
    </div>
    <div class="mx-[18px] border-t-2 border-dashed border-white/20" />
    <div class="flex items-center justify-between px-5 py-3.5 text-xs text-mut">
      <span>{{ pie ?? "Festival 2027" }}</span>
      <span class="ticket-bars" aria-hidden="true" />
    </div>
  </article>
</template>
