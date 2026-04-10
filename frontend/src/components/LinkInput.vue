<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { parseStream } from '../api/client'
import type { StreamInfo } from '../types'

const emit = defineEmits<{ play: [info: StreamInfo] }>()

const url = ref('')
const loading = ref(false)

async function handleParse() {
  const trimmed = url.value.trim()
  if (!trimmed) return
  loading.value = true
  try {
    const info = await parseStream(trimmed)
    if (!info.is_live) {
      ElMessage.warning('该主播当前未在直播')
      return
    }
    if (!info.stream_url) {
      ElMessage.warning(
        info.hint?.trim() ||
          '在播但未拿到播放地址，请检查网络或按平台要求配置 Cookie / 代理。',
      )
      return
    }
    emit('play', info)
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '解析失败，请检查链接')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="link-input">
    <el-input
      v-model="url"
      placeholder="粘贴直播间链接，支持抖音、斗鱼、B站等 40+ 平台"
      size="large"
      clearable
      :prefix-icon="Search"
      @keyup.enter="handleParse"
      :disabled="loading"
    />
    <el-button
      type="primary"
      size="large"
      :loading="loading"
      @click="handleParse"
    >
      观看
    </el-button>
  </div>
</template>

<style scoped>
.link-input {
  display: flex;
  gap: 8px;
  flex: 1;
  max-width: 700px;
}
</style>
