export interface StreamInfo {
  platform: string
  room_id: string
  nickname: string
  title: string
  stream_url: string
  is_live: boolean
  avatar?: string
  room_url: string
  /** Backend hint when is_live but stream_url is empty (e.g. Douyu cookie / Node.js). */
  hint?: string | null
}

export interface FavoriteItem {
  id: number
  room_url: string
  room_id: string
  platform: string
  nickname: string
  avatar?: string
  is_live: boolean
  title?: string
  stream_url?: string
  last_live_at?: string
  created_at: string
}

export interface WSEvent {
  event: 'live_start' | 'live_end'
  room_id: string
  platform: string
  nickname: string
  title?: string
  stream_url?: string
}
