from fastapi import APIRouter, HTTPException

from app.core.database import add_favorite, remove_favorite, get_all_favorites
from app.models.schemas import FavoriteAdd, FavoriteRemove, FavoriteItem
from app.services.parser import parse_stream, detect_platform
from app.services.stream import extract_stream_info

router = APIRouter()


@router.get("/favorites", response_model=list[FavoriteItem])
async def list_favorites():
    rows = await get_all_favorites()
    items: list[FavoriteItem] = []
    for row in rows:
        url = row["room_url"]
        is_live = False
        title = None
        stream_url = None
        try:
            raw = await parse_stream(url)
            info = extract_stream_info(raw)
            is_live = info.is_live
            title = info.title
            stream_url = info.stream_url if info.is_live else None
        except Exception:
            pass
        items.append(
            FavoriteItem(
                id=row["id"],
                room_url=row["room_url"],
                room_id=row["room_id"],
                platform=row["platform"],
                nickname=row["nickname"],
                avatar=row["avatar"],
                is_live=is_live,
                title=title,
                stream_url=stream_url,
                last_live_at=row["last_live_at"],
                created_at=row["created_at"],
            )
        )
    return items


@router.post("/favorite/add", response_model=dict)
async def add_fav(body: FavoriteAdd):
    det = detect_platform(body.room_url)
    if det is None:
        raise HTTPException(status_code=400, detail="Unsupported platform URL")
    row_id = await add_favorite(
        room_url=body.room_url,
        room_id=body.room_id,
        platform=body.platform,
        nickname=body.nickname,
        avatar=body.avatar,
    )
    return {"id": row_id, "ok": True}


@router.post("/favorite/remove", response_model=dict)
async def remove_fav(body: FavoriteRemove):
    deleted = await remove_favorite(body.room_url)
    if not deleted:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"ok": True}
