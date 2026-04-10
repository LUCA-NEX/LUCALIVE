import { ref, onUnmounted } from 'vue'
import type { WSEvent } from '../types'

export function useWebSocket(onEvent: (evt: WSEvent) => void) {
  const connected = ref(false)
  let ws: WebSocket | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null

  function connect() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws'
    ws = new WebSocket(`${proto}://${location.host}/ws/status`)

    ws.onopen = () => {
      connected.value = true
    }

    ws.onmessage = (e) => {
      try {
        const data: WSEvent = JSON.parse(e.data)
        onEvent(data)
      } catch { /* ignore malformed */ }
    }

    ws.onclose = () => {
      connected.value = false
      reconnectTimer = setTimeout(connect, 3000)
    }

    ws.onerror = () => {
      ws?.close()
    }
  }

  connect()

  onUnmounted(() => {
    if (reconnectTimer) clearTimeout(reconnectTimer)
    ws?.close()
  })

  return { connected }
}
