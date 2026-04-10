from fastapi import APIRouter, HTTPException

from app.models.schemas import ParseRequest, StreamInfo
from app.services.parser import parse_stream
from app.services.stream import extract_stream_info, no_stream_hint

router = APIRouter()


@router.post("/parse", response_model=StreamInfo)
async def parse_url(body: ParseRequest):
    try:
        raw = await parse_stream(body.url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Upstream parse error: {exc}")
    info = extract_stream_info(raw)
    if info.is_live and not (info.stream_url or "").strip():
        return info.model_copy(update={"hint": no_stream_hint(info.platform, raw)})
    return info
