<script setup lang="ts">
import { computed } from 'vue'
import { StarFilled, Loading } from '@element-plus/icons-vue'
import { useFavoritesStore } from '../stores/favorites'
import type { StreamInfo } from '../types'
import FavoriteCard from './FavoriteCard.vue'

const props = defineProps<{ currentStream: StreamInfo | null }>()
const emit = defineEmits<{ play: [info: StreamInfo] }>()

const favStore = useFavoritesStore()

const sortedItems = computed(() => {
  return [...favStore.items].sort((a, b) => {
    if (a.is_live && !b.is_live) return -1
    if (!a.is_live && b.is_live) return 1
    return 0
  })
})

function handleRemove(room_url: string) {
  favStore.remove(room_url)
}
</script>

<template>
  <div class="fav-list">
    <div class="fav-header">
      <el-icon :size="16"><StarFilled /></el-icon>
      <span>收藏列表</span>
      <span class="fav-count">{{ favStore.items.length }}</span>
      <el-button
        text
        size="small"
        :loading="favStore.loading"
        @click="favStore.load()"
      >
        刷新
      </el-button>
    </div>

    <div v-if="favStore.loading && favStore.items.length === 0" class="fav-empty">
      <el-icon class="spin" :size="24"><Loading /></el-icon>
      <p>加载中...</p>
    </div>

    <div v-else-if="favStore.items.length === 0" class="fav-empty">
      <p>暂无收藏</p>
      <p class="fav-hint">观看直播时点击星标收藏主播</p>
    </div>

    <template v-else>
      <FavoriteCard
        v-for="item in sortedItems"
        :key="item.id"
        :item="item"
        :active="currentStream?.room_url === item.room_url"
        @play="emit('play', $event)"
        @remove="handleRemove"
      />
    </template>
  </div>
</template>

<style scoped>
.fav-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.fav-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 14px;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}

.fav-count {
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 11px;
  padding: 1px 8px;
  border-radius: 10px;
}

.fav-header .el-button {
  margin-left: auto;
}

.fav-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-secondary);
  padding: 40px 20px;
}

.fav-hint {
  font-size: 12px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
