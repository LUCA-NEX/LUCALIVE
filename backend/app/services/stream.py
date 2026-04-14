"""
Extract the best playable stream URL from raw spider data.

DouyinLiveRecorder spiders return inconsistent shapes: e.g. Douyin uses ``status == 2``
for live and puts URLs under ``stream_url.hls_pull_url_map`` / ``flv_pull_url``, and does
not set ``is_live``. We normalize that here so the API matches what the UI expects.
"""
from __future__ import annotations

import shutil
from typing import Any

from app.core.config import BASE_DIR, REPO_ROOT, get_douyu_cookies
from app.models.schemas import StreamInfo


def _infer_is_live(raw: dict) -> bool:
    if raw.get("is_live") is True:
        return True
    # Douyin web/app room payload: 2 = broadcasting
    if raw.get("status") == 2:
        return True
    # Bilibili-style room info
    ls = raw.get("live_status")
    if ls is True or ls == 1:
        return True
    if isinstance(ls, str) and ls.upper() == "ON":
        return True
    # Some spiders use numeric type + flag
    if raw.get("type") == 2 and raw.get("is_live"):
        return True
    return False


def _douyin_nested_urls(raw: dict) -> tuple[str, str]:
    ss = raw.get("stream_url")
    if not isinstance(ss, dict):
        return "", ""
    hls_map = ss.get("hls_pull_url_map") or {}
    flv_map = ss.get("flv_pull_url") or {}
    m3u8 = ""
    if "ORIGIN" in hls_map:
        m3u8 = hls_map["ORIGIN"]
    elif hls_map:
        m3u8 = next(iter(hls_map.values()))
    flv = ""
    if "ORIGIN" in flv_map:
        flv = flv_map["ORIGIN"]
    elif flv_map:
        flv = next(iter(flv_map.values()))
    return m3u8, flv


def _extract_stream_url(raw: dict, is_live: bool, platform: str) -> str:
    if not is_live:
        return ""
    # Huya's spider already selects a browser-friendly CDN/protocol in `record_url`.
    # The first `m3u8_url` in the payload can stall in the web player.
    direct_candidates = (
        (raw.get("record_url"), raw.get("m3u8_url"), raw.get("flv_url"), raw.get("live_url"), raw.get("play_url"))
        if platform == "huya"
        else (raw.get("m3u8_url"), raw.get("flv_url"), raw.get("record_url"), raw.get("live_url"), raw.get("play_url"))
    )
    direct = next((url for url in direct_candidates if isinstance(url, str) and url.strip()), "")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    dm3, dflv = _douyin_nested_urls(raw)
    return dm3 or dflv or ""


def _room_id(raw: dict) -> str:
    for key in ("room_id", "id_str", "id"):
        v = raw.get(key)
        if v is not None and str(v).strip():
            return str(v).strip()
    return ""


def extract_stream_info(raw: dict) -> StreamInfo:
    """Normalise the heterogeneous dicts returned by various spider functions."""
    platform = raw.get("_platform", "unknown")
    room_url = raw.get("_room_url", "")
    anchor_name = raw.get("anchor_name", "") or ""
    is_live = _infer_is_live(raw)
    title = (
        raw.get("title")
        or raw.get("room_title")
        or raw.get("introduction")
        or ""
    )
    if not isinstance(title, str):
        title = str(title) if title is not None else ""
    room_id = _room_id(raw)
    stream_url = _extract_stream_url(raw, is_live, platform)

    return StreamInfo(
        platform=platform,
        room_id=room_id,
        nickname=anchor_name,
        title=title or "",
        stream_url=stream_url,
        is_live=is_live,
        room_url=room_url,
    )


def normalize_spider_result(data: Any) -> dict:
    """Spider functions may return a dict, a bare URL string, or None on failure."""
    if isinstance(data, dict):
        return data
    if isinstance(data, str) and data.strip():
        return {
            "anchor_name": "",
            "is_live": True,
            "record_url": data.strip(),
        }
    if data is None:
        return {"anchor_name": "", "is_live": False}
    if isinstance(data, list):
        if len(data) == 1 and isinstance(data[0], dict):
            return data[0]
        return {"anchor_name": "", "is_live": False}
    return {"anchor_name": "", "is_live": False}


def no_stream_hint(platform: str, raw: dict | None = None) -> str:
    """Shown when room is live but no playable URL was resolved (platform-specific guidance)."""
    if platform == "douyu":
        raw = raw or {}
        ck = get_douyu_cookies()
        node = shutil.which("node") or shutil.which("node.exe")
        parts: list[str] = ["斗鱼：房间在播但未拿到拉流地址。"]
        if ck:
            parts.append(f"后端已读到 LUCALIVE_DOUYU_COOKIES（约 {len(ck)} 字符）。")
        else:
            parts.append(
                "后端**未**读到 LUCALIVE_DOUYU_COOKIES。请在仓库根目录或 backend 目录创建 .env，"
                f"或设置系统环境变量（已尝试加载 {REPO_ROOT / '.env'} 与 {BASE_DIR / '.env'}），"
                "然后**彻底关掉并重启**运行 uvicorn 的终端/IDE。"
            )
        if node:
            parts.append(f"PATH 中已找到 Node：{node}。")
        else:
            parts.append("PATH 中未找到 node/node.exe，斗鱼签名会失败；请安装 Node.js 并重启终端。")
        if raw.get("_douyu_last_msg"):
            parts.append(f"接口/异常：{raw['_douyu_last_msg']}")
        parts.append("仍失败时可用 DouyinLiveRecorder 自带 demo 对比同一房间是否可拉流。")
        return "".join(parts)
    if platform == "douyin":
        return (
            "抖音：在播但未解析到播放地址。部分玩法仅支持 App 分享链接，或需在服务端配置 Cookie / 代理以通过风控。"
        )
    return "在播但未解析到播放地址，请稍后重试，或检查网络、Cookie、代理设置。"
