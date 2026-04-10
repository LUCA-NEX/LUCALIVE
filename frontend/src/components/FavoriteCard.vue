<script setup lang="ts">
import { computed } from 'vue'
import { Star, VideoPlay } from '@element-plus/icons-vue'
import type { FavoriteItem, StreamInfo } from '../types'
import RacingBadge from './RacingBadge.vue'

const RACING_RE = /WRC|Hyundai|i20|N\s?Line/i

const props = defineProps<{
  item: FavoriteItem
  active: boolean
}>()

const emit = defineEmits<{
  play: [info: StreamInfo]
  remove: [room_url: string]
}>()

const isRacing = computed(() => {
  return props.item.is_live && props.item.title ? RACING_RE.test(props.item.title) : false
})

const platformColor = computed(() => {
  switch (props.item.platform) {
    case 'douyin': return 'var(--douyin-red)'
    case 'douyu': return 'var(--douyu-red)'
    default: return 'var(--accent-blue)'
  }
})

function handlePlay() {
  if (!props.item.is_live || !props.item.stream_url) return
  emit('play', {
    platform: props.item.platform,
    room_id: props.item.room_id,
    nickname: props.item.nickname,
    title: props.item.title || '',
    stream_url: props.item.stream_url!,
    is_live: true,
    room_url: props.item.room_url,
  })
}
</script>

<template>
  <div
    class="fav-card"
    :class="{ 'is-live': item.is_live, 'is-active': active, 'racing-glow': isRacing }"
    @click="handlePlay"
  >
    <div class="card-avatar">
      <div class="avatar-circle" :style="{ borderColor: item.is_live ? platformColor : 'var(--border-color)' }">
        {{ item.nickname.charAt(0) }}
      </div>
      <span v-if="item.is_live" class="live-dot" />
    </div>

    <div class="card-info">
      <div class="card-top">
        <span class="card-name">{{ item.nickname }}</span>
        <RacingBadge :active="isRacing" />
        <span class="card-platform" :style="{ color: platformColor }">{{ item.platform }}</span>
      </div>
      <div class="card-bottom">
        <template v-if="item.is_live">
          <el-icon :size="12" color="var(--live-green)"><VideoPlay /></el-icon>
          <span class="card-title">{{ item.title || '直播中' }}</span>
        </template>
        <template v-else>
          <span class="card-offline">未开播</span>
          <span v-if="item.last_live_at" class="card-last">上次: {{ item.last_live_at }}</span>
        </template>
      </div>
    </div>

    <el-button
      class="card-remove"
      :icon="Star"
      circle
      size="small"
      type="warning"
      @click.stop="emit('remove', item.room_url)"
    />
  </div>
</template>

<style scoped>
.fav-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-color);
  cursor: default;
  transition: background 0.15s;
}

.fav-card.is-live {
  cursor: pointer;
}

.fav-card.is-live:hover,
.fav-card.is-active {
  background: var(--bg-card-hover);
}

.card-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--border-color);
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: var(--text-primary);
}

.live-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--live-green);
  border: 2px solid var(--bg-secondary);
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-top {
  display: flex;
  align-items: center;
  gap: 6px;
}

.card-name {
  font-weight: 600;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-platform {
  margin-left: auto;
  font-size: 10px;
  text-transform: uppercase;
  font-weight: 600;
  flex-shrink: 0;
}

.card-bottom {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 3px;
  font-size: 12px;
  color: var(--text-secondary);
}

.card-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-offline {
  color: var(--text-secondary);
}

.card-last {
  margin-left: auto;
  font-size: 11px;
  flex-shrink: 0;
}

.card-remove {
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.15s;
}

.fav-card:hover .card-remove {
  opacity: 1;
}
</style>
