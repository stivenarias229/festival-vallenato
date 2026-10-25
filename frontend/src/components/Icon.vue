<script setup lang="ts">
const paths: Record<string, string> = {
  home: '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
  ticket:
    '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z"/><path d="M14 7v10" stroke-dasharray="2 2"/>',
  vote: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
  users:
    '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.3-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c2.6 0 4.2 1.6 4.8 4.5"/>',
  chart: '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
  grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  music: '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
  mic: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
  accordion:
    '<rect x="2" y="6" width="4" height="12" rx="1"/><rect x="18" y="6" width="4" height="12" rx="1"/><path d="M6 7l2 10 2-10 2 10 2-10 2 10 2-10"/>',
  acc: '<rect x="2" y="6" width="4" height="12" rx="1"/><rect x="18" y="6" width="4" height="12" rx="1"/><path d="M6 7l2 10 2-10 2 10 2-10 2 10 2-10"/>',
  star: '<path d="M12 3l2.2 5.3L20 9l-4.2 3.8L17 18.5 12 15.5 7 18.5l1.2-5.7L4 9l5.8-.7z"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
  chevron: '<path d="M9 6l6 6-6 6"/>',
  chev: '<path d="M9 6l6 6-6 6"/>',
  back: '<path d="M15 6l-6 6 6 6"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7"/>',
  edit: '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
  up: '<path d="M12 19V5M6 11l6-6 6 6"/>',
  down: '<path d="M12 5v14M6 13l6 6 6-6"/>',
  download: '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
  dl: '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
  close: '<path d="M6 6l12 12M18 6L6 18"/>',
  alert: '<circle cx="12" cy="12" r="9"/><path d="M12 8v5"/><path d="M12 16.5h.01"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6"/><path d="M12 8h.01"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
}

export type IconName = keyof typeof paths

const props = withDefaults(
  defineProps<{
    name: IconName | string
    size?: number
  }>(),
  { size: 24 },
)

const markup = paths[props.name] ?? ""
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    v-html="markup"
  />
</template>
