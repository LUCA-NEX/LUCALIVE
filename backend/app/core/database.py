from __future__ import annotations

import aiosqlite

from app.core.config import DB_PATH

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS favorites (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    room_url   TEXT    UNIQUE NOT NULL,
    room_id    TEXT    NOT NULL,
    platform   TEXT    NOT NULL,
    nickname   TEXT    NOT NULL,
    avatar     TEXT    DEFAULT '',
    last_live_at TEXT  DEFAULT NULL,
    created_at TEXT    DEFAULT (datetime('now','localtime'))
);
"""


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db() -> None:
    db = await get_db()
    try:
        await db.execute(CREATE_TABLE_SQL)
        await db.commit()
    finally:
        await db.close()


async def add_favorite(
    room_url: str,
    room_id: str,
    platform: str,
    nickname: str,
    avatar: str | None = None,
) -> int:
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT OR IGNORE INTO favorites (room_url, room_id, platform, nickname, avatar) "
            "VALUES (?, ?, ?, ?, ?)",
            (room_url, room_id, platform, nickname, avatar or ""),
        )
        await db.commit()
        return cursor.lastrowid or 0
    finally:
        await db.close()


async def remove_favorite(room_url: str) -> bool:
    db = await get_db()
    try:
        cursor = await db.execute(
            "DELETE FROM favorites WHERE room_url = ?", (room_url,)
        )
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def get_all_favorites() -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id, room_url, room_id, platform, nickname, avatar, last_live_at, created_at "
            "FROM favorites ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def update_last_live(room_url: str, last_live_at: str) -> None:
    db = await get_db()
    try:
        await db.execute(
            "UPDATE favorites SET last_live_at = ? WHERE room_url = ?",
            (last_live_at, room_url),
        )
        await db.commit()
    finally:
        await db.close()
