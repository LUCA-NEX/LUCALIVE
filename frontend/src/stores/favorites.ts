import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FavoriteItem, StreamInfo } from '../types'
import { getFavorites, addFavorite, removeFavorite } from '../api/client'

export const useFavoritesStore = defineStore('favorites', () => {
  const items = ref<FavoriteItem[]>([])
  const loading = ref(false)

  async function load() {
    loading.value = true
    try {
      items.value = await getFavorites()
    } finally {
      loading.value = false
    }
  }

  async function add(info: StreamInfo) {
    await addFavorite({
      room_url: info.room_url,
      platform: info.platform,
      nickname: info.nickname,
      room_id: info.room_id,
      avatar: info.avatar,
    })
    await load()
  }

  async function remove(room_url: string) {
    await removeFavorite(room_url)
    items.value = items.value.filter((i) => i.room_url !== room_url)
  }

  function updateStatus(room_id: string, platform: string, is_live: boolean, title?: string, stream_url?: string) {
    const item = items.value.find((i) => i.room_id === room_id && i.platform === platform)
    if (item) {
      item.is_live = is_live
      item.title = title ?? item.title
      item.stream_url = stream_url ?? item.stream_url
    }
  }

  return { items, loading, load, add, remove, updateStatus }
})
