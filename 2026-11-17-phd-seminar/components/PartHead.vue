<script setup lang="ts">
// The head of a part's panel on the overview: its number and the keyword that the talk's
// title uses for the part, with the tool's name as a dark mark beside it, as in the
// picture of the Conclusion panel. A part without a keyword shows its name as the head.
defineProps<{ no: number, name: string, keyword?: string }>()
</script>

<template>
  <div class="head">
    <div class="name"><span class="no">{{ no }}</span>{{ keyword || name }}</div>
    <div v-if="keyword" class="tool">{{ name }}</div>
  </div>
</template>

<style scoped>
.head { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.name { font-size: 34px; font-weight: 700; line-height: 1.4; white-space: nowrap; }
.no { margin-right: 18px; color: var(--aau-dark); font-variant-numeric: tabular-nums; }
.tool { flex: none; padding: 6px 16px; border-radius: 8px; background: var(--aau-dark); color: #fff; font-size: 22px; font-weight: 700; }
</style>
