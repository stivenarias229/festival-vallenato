<script setup lang="ts">
import Spinner from "@/components/Spinner.vue"

const model = defineModel<boolean>({ default: false })

withDefaults(
  defineProps<{
    label?: string
    disabled?: boolean
    loading?: boolean
  }>(),
  { disabled: false, loading: false },
)
</script>

<template>
  <label class="relative mx-auto block h-[26px] w-[46px] shrink-0">
    <span v-if="label" class="sr-only">{{ label }}</span>
    <input
      v-model="model"
      type="checkbox"
      class="absolute inset-0 z-1 h-full w-full cursor-pointer opacity-0 disabled:cursor-not-allowed"
      :disabled="disabled || loading"
      role="switch"
      :aria-checked="model"
      :aria-busy="loading || undefined"
    />
    <span
      class="absolute inset-0 rounded-full bg-white/15 transition-colors duration-200 after:absolute after:top-[3px] after:left-[3px] after:size-5 after:rounded-full after:bg-white after:transition-all after:duration-200"
      :class="[
        model ? 'bg-gold after:left-[23px]' : '',
        loading ? 'opacity-35' : '',
      ]"
    />
    <span
      v-if="loading"
      class="absolute inset-0 z-2 grid place-items-center text-gold"
    >
      <Spinner :size="14" />
    </span>
  </label>
</template>
