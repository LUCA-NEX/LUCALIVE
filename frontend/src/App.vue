<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { StreamInfo, WSEvent } from './types'
import { useFavoritesStore } from './stores/favorites'
import { useWebSocket } from './composables/useWebSocket'
import { useNotification } from './composables/useNotification'
import LinkInput from './components/LinkInput.vue'
import VideoPlayer from './components/VideoPlayer.vue'
import FavoriteList from './components/FavoriteList.vue'

const favStore = useFavoritesStore()
const { notify } = useNotification()

const currentStream = ref<StreamInfo | null>(null)

const isFavorited = computed(() => {
  if (!currentStream.value) return false
  return favStore.items.some((i) => i.room_url === currentStream.value!.room_url)
})

function handlePlay(info: StreamInfo) {
  currentStream.value = info
}

async function toggleFavorite() {
  if (!currentStream.value) return
  if (isFavorited.value) {
    await favStore.remove(currentStream.value.room_url)
    ElMessage.success('已取消收藏')
  } else {
    await favStore.add(currentStream.value)
    ElMessage.success('已收藏')
  }
}

useWebSocket((evt: WSEvent) => {
  if (evt.event === 'live_start') {
    notify(evt)
    favStore.updateStatus(evt.room_id, evt.platform, true, evt.title, evt.stream_url)
  } else if (evt.event === 'live_end') {
    favStore.updateStatus(evt.room_id, evt.platform, false)
  }
})

onMounted(() => {
  favStore.load()
})
</script>

<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="brand">
        <span class="brand-logo">▶</span>
        <h1 class="brand-title">LUCALIVE</h1>
        <span class="brand-sub">一个网站，多平台直播</span>
      </div>
      <LinkInput @play="handlePlay" />
    </header>

    <main class="app-main">
      <section class="player-section">
        <VideoPlayer :stream="currentStream" />
        <div v-if="currentStream" class="now-playing">
          <span class="live-badge" v-if="currentStream.is_live">LIVE</span>
          <span class="now-nickname">{{ currentStream.nickname }}</span>
          <span class="now-title" v-if="currentStream.title">{{ currentStream.title }}</span>
          <span class="now-platform">{{ currentStream.platform }}</span>
          <el-button
            :icon="isFavorited ? StarFilled : Star"
            circle
            size="small"
            :type="isFavorited ? 'warning' : 'default'"
            @click="toggleFavorite"
          />
        </div>
        <div v-else class="player-placeholder">
          <p>粘贴直播间链接，即刻开始观看</p>
        </div>
      </section>

      <aside class="sidebar">
        <FavoriteList
          :current-stream="currentStream"
          @play="handlePlay"
        />
      </aside>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.app-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 12px 24px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.brand-logo {
  font-size: 24px;
  color: var(--accent-blue);
}

.brand-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
}

.brand-sub {
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.player-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.now-playing {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 24px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  font-size: 14px;
}

.live-badge {
  background: #e53935;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 3px;
  letter-spacing: 1px;
}

.now-nickname {
  font-weight: 600;
}

.now-title {
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.now-platform {
  margin-left: auto;
  color: var(--accent-blue);
  font-size: 12px;
  text-transform: uppercase;
}

.player-placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 16px;
}

.sidebar {
  width: 320px;
  flex-shrink: 0;
  border-left: 1px solid var(--border-color);
  overflow-y: auto;
  background: var(--bg-secondary);
}
</style>
