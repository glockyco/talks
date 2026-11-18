<script setup lang="ts">
import { talk } from '../talk'

// The research question from talk.ts in a dark panel: large on the overview, with its line
// break, and compact on one line above a picture.
defineProps<{ compact?: boolean }>()
</script>

<template>
  <div v-if="compact" class="ask compact">{{ talk.questionLines.join(' ') }}</div>
  <div v-else class="ask"><template v-for="(l, i) in talk.questionLines" :key="i"><br v-if="i > 0">{{ l }}</template></div>
</template>

<style scoped>
.ask { padding: 34px 40px 38px; border-radius: 16px; background: var(--aau-dark); color: #fff; font-size: var(--fs-lead); line-height: 1.35; font-weight: 700; text-align: center; }
.ask.compact { padding: 22px 32px 24px; font-size: var(--fs-body); line-height: 1.3; }
</style>
