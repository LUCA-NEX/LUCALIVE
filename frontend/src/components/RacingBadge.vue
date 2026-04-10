<script setup lang="ts">
defineProps<{ active: boolean }>()
</script>

<template>
  <span v-if="active" class="racing-badge">WRC</span>
</template>

<style scoped>
.racing-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  color: #fff;
  background: var(--accent-blue);
  padding: 1px 6px;
  border-radius: 3px;
  letter-spacing: 1px;
  animation: breathing 2s ease-in-out infinite;
}
</style>
