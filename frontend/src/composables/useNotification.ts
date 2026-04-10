import { ElNotification } from 'element-plus'
import type { WSEvent } from '../types'

let permissionGranted = false

export function useNotification() {
  async function requestPermission() {
    if (!('Notification' in window)) return
    if (Notification.permission === 'granted') {
      permissionGranted = true
    } else if (Notification.permission !== 'denied') {
      const result = await Notification.requestPermission()
      permissionGranted = result === 'granted'
    }
  }

  function notify(evt: WSEvent) {
    const title = `${evt.nickname} 开播了！`
    const body = evt.title || `${evt.platform} 直播中`

    if (permissionGranted) {
      new Notification(title, { body, icon: '/favicon.svg' })
    } else {
      ElNotification({
        title,
        message: body,
        type: 'success',
        duration: 5000,
      })
    }
  }

  requestPermission()

  return { notify }
}
