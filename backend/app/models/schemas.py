from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ParseRequest(BaseModel):
    url: str


class StreamInfo(BaseModel):
    platform: str
    room_id: str
    nickname: str
    title: str
    stream_url: str
    is_live: bool
    avatar: Optional[str] = None
    room_url: str = ""
    hint: Optional[str] = None


class FavoriteAdd(BaseModel):
    room_url: str
    platform: str
    nickname: str
    room_id: str
    avatar: Optional[str] = None


class FavoriteRemove(BaseModel):
    room_url: str


class FavoriteItem(BaseModel):
    id: int
    room_url: str
    room_id: str
    platform: str
    nickname: str
    avatar: Optional[str] = None
    is_live: bool = False
    title: Optional[str] = None
    stream_url: Optional[str] = None
    last_live_at: Optional[str] = None
    created_at: str = ""


class WSEvent(BaseModel):
    event: str
    room_id: str
    platform: str
    nickname: str
    title: Optional[str] = None
    stream_url: Optional[str] = None
