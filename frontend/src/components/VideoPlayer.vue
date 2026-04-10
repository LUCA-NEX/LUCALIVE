<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from 'vue'
import Artplayer from 'artplayer'
import Hls from 'hls.js'
import mpegts from 'mpegts.js'
import type { StreamInfo } from '../types'

const props = defineProps<{ stream: StreamInfo | null }>()

const containerRef = ref<HTMLDivElement>()
let art: Artplayer | null = null

function detectType(url: string): string {
  if (url.includes('.m3u8') || url.includes('m3u8')) return 'm3u8'
  if (url.includes('.flv') || url.includes('flv')) return 'flv'
  return 'm3u8'
}

function destroyPlayer() {
  if (art) {
    art.destroy()
    art = null
  }
}

function createPlayer(url: string) {
  if (!containerRef.value) return
  destroyPlayer()

  const type = detectType(url)

  art = new Artplayer({
    container: containerRef.value,
    url,
    type,
    isLive: true,
    autoplay: true,
    autoSize: false,
    fullscreen: true,
    pip: true,
    screenshot: true,
    setting: true,
    mutex: true,
    theme: '#0078d4',
    customType: {
      m3u8(video: HTMLVideoElement, src: string, player: Artplayer) {
        if ((player as any)._mpegts) {
          (player as any)._mpegts.destroy()
          ;(player as any)._mpegts = null
        }
        if (Hls.isSupported()) {
          if ((player as any)._hls) (player as any)._hls.destroy()
          const hls = new Hls({ enableWorker: true })
          hls.loadSource(src)
          hls.attachMedia(video)
          ;(player as any)._hls = hls
          player.on('destroy', () => hls.destroy())
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
          video.src = src
        }
      },
      flv(video: HTMLVideoElement, src: string, player: Artplayer) {
        if ((player as any)._hls) {
          (player as any)._hls.destroy()
          ;(player as any)._hls = null
        }
        if (mpegts.isSupported()) {
          if ((player as any)._mpegts) (player as any)._mpegts.destroy()
          const instance = mpegts.createPlayer({ type: 'flv', url: src, isLive: true })
          instance.attachMediaElement(video)
          instance.load()
          ;(player as any)._mpegts = instance
          player.on('destroy', () => instance.destroy())
        }
      },
    },
  })
}

watch(
  () => props.stream,
  (s) => {
    if (s?.stream_url) {
      createPlayer(s.stream_url)
    } else {
      destroyPlayer()
    }
  },
)

onBeforeUnmount(destroyPlayer)
</script>

<template>
  <div class="video-wrapper">
    <div ref="containerRef" class="video-container" />
  </div>
</template>

<style scoped>
.video-wrapper {
  flex: 1;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
}

.video-container {
  width: 100%;
  height: 100%;
}
</style>
