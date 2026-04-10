"""
Background task: poll all favorites every POLL_INTERVAL_SECONDS and broadcast
status changes via WebSocket.
"""
from __future__ import annotations

import asyncio
from datetime import datetime

from loguru import logger

from app.core.config import POLL_INTERVAL_SECONDS
from app.core.database import get_all_favorites, update_last_live
from app.services.parser import parse_stream
from app.services.stream import extract_stream_info
from app.api.ws import broadcast

_status_cache: dict[str, bool] = {}


async def _poll_once() -> None:
    rows = await get_all_favorites()
    for row in rows:
        url = row["room_url"]
        try:
            raw = await parse_stream(url)
            info = extract_stream_info(raw)
        except Exception as exc:
            logger.warning(f"Watcher poll error for {url}: {exc}")
            continue

        prev_live = _status_cache.get(url, False)
        now_live = info.is_live

        if now_live and not prev_live:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await update_last_live(url, now_str)
            await broadcast(
                {
                    "event": "live_start",
                    "room_id": row["room_id"],
                    "platform": row["platform"],
                    "nickname": row["nickname"],
                    "title": info.title,
                    "stream_url": info.stream_url,
                }
            )
            logger.info(f"[LIVE] {row['nickname']} ({row['platform']}) is now live")

        if not now_live and prev_live:
            await broadcast(
                {
                    "event": "live_end",
                    "room_id": row["room_id"],
                    "platform": row["platform"],
                    "nickname": row["nickname"],
                    "title": "",
                    "stream_url": "",
                }
            )

        _status_cache[url] = now_live


async def start_watcher() -> None:
    logger.info(f"Watcher started (interval={POLL_INTERVAL_SECONDS}s)")
    while True:
        try:
            await _poll_once()
        except Exception as exc:
            logger.error(f"Watcher loop error: {exc}")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
