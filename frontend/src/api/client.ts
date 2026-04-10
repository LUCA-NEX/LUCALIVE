import axios from 'axios'
import type { StreamInfo, FavoriteItem } from '../types'

const http = axios.create({ baseURL: '/api', timeout: 30000 })

export async function parseStream(url: string): Promise<StreamInfo> {
  const { data } = await http.post<StreamInfo>('/parse', { url })
  return data
}

export async function getFavorites(): Promise<FavoriteItem[]> {
  const { data } = await http.get<FavoriteItem[]>('/favorites')
  return data
}

export async function addFavorite(item: {
  room_url: string
  platform: string
  nickname: string
  room_id: string
  avatar?: string
}): Promise<{ id: number; ok: boolean }> {
  const { data } = await http.post('/favorite/add', item)
  return data
}

export async function removeFavorite(room_url: string): Promise<{ ok: boolean }> {
  const { data } = await http.post('/favorite/remove', { room_url })
  return data
}
