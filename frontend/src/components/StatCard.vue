<script setup lang="ts">
defineProps<{
  valor: string | number
  etiqueta: string
}>()
</script>

<template>
  <div class="rounded-[18px] border border-ln bg-linear-to-[160deg] from-s2 to-s1 px-1.5 py-3.5 text-center text-[11px] text-mut">
    <b class="block font-serif text-[27px] font-semibold text-gold-2">{{ valor }}</b>
    {{ etiqueta }}
  </div>
</template>
