<script setup lang="ts">
import { computed } from "vue"
import { Link } from "@inertiajs/vue3"

import Spinner from "@/components/Spinner.vue"

const props = withDefaults(
  defineProps<{
    variant?: "primary" | "secondary" | "gold-outline"
    href?: string
    type?: "button" | "submit"
    disabled?: boolean
    loading?: boolean
    size?: "default" | "mini"
  }>(),
  { variant: "primary", type: "button", disabled: false, loading: false, size: "default" },
)

const bloqueado = computed(() => props.disabled || props.loading)
</script>

<template>
  <component
    :is="href && !bloqueado ? Link : href ? 'a' : 'button'"
    :href="href"
    :type="href ? undefined : type"
    :disabled="bloqueado"
    :aria-busy="loading || undefined"
    :aria-disabled="bloqueado || undefined"
    :class="[
      'inline-flex items-center justify-center gap-2 no-underline transition-transform',
      size === 'mini'
        ? 'min-h-11 min-w-11 w-auto rounded-[10px] px-2.5 py-1.5 text-xs font-bold tracking-normal'
        : 'min-h-11 w-full rounded-[15px] px-4 py-3.5 text-[15px] font-extrabold tracking-[0.03em]',
      variant === 'primary' &&
        'bg-linear-to-b from-gold-2 to-[#d8a23f] text-ink shadow-[0_10px_26px_#e2b75f3a,inset_0_1px_0_#fff7]',
      variant === 'secondary' && 'border border-white/30 bg-white/5 text-ivory shadow-none',
      variant === 'gold-outline' && 'border border-gold/40 bg-white/5 text-gold shadow-none',
      'active:translate-y-0.5 disabled:pointer-events-none disabled:opacity-35',
    ]"
  >
    <Spinner v-if="loading" :size="size === 'mini' ? 14 : 18" />
    <slot />
  </component>
</template>
