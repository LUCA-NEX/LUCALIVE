"""
URL dispatch: detect platform from URL and call the corresponding spider function.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Callable, Awaitable

from app.core.config import DOUYINLIVERECORDER_PATH, get_douyu_cookies
from app.services.stream import normalize_spider_result

_dlr_path = Path(DOUYINLIVERECORDER_PATH)
if str(_dlr_path) not in sys.path:
    sys.path.insert(0, str(_dlr_path))

from src import spider  # noqa: E402  – DouyinLiveRecorder
from src import stream as dlr_stream  # noqa: E402

from app.services import douyu_token  # noqa: E402

douyu_token.patch_spider_get_token_js()

PlatformFunc = Callable[..., Awaitable[Any]]

PLATFORM_MAP: list[tuple[str, str, PlatformFunc]] = [
    (r"live\.douyin\.com|douyin\.com", "douyin", spider.get_douyin_app_stream_data),
    (r"douyu\.com", "douyu", spider.get_douyu_info_data),
    (r"live\.bilibili\.com", "bilibili", spider.get_bilibili_stream_data),
    (r"live\.kuaishou\.com", "kuaishou", spider.get_kuaishou_stream_data),
    (r"huya\.com", "huya", spider.get_huya_app_stream_url),
    (r"twitch\.tv", "twitch", spider.get_twitchtv_stream_data),
    (r"tiktok\.com", "tiktok", spider.get_tiktok_stream_data),
    (r"yy\.com", "yy", spider.get_yy_stream_data),
    (r"xiaohongshu\.com", "xhs", spider.get_xhs_stream_url),
    (r"bigo\.tv", "bigo", spider.get_bigo_stream_url),
    (r"cc\.163\.com", "netease", spider.get_netease_stream_data),
    (r"live\.acfun\.cn", "acfun", spider.get_acfun_stream_data),
    (r"showroom-live\.com", "showroom", spider.get_showroom_stream_data),
    (r"youtube\.com|youtu\.be", "youtube", spider.get_youtube_stream_url),
    (r"17\.live", "17live", spider.get_17live_stream_url),
    (r"chzzk\.naver\.com", "chzzk", spider.get_chzzk_stream_data),
    (r"sooplive\.co\.kr", "sooplive", spider.get_sooplive_stream_data),
    (r"pandalive\.co\.kr", "pandatv", spider.get_pandatv_stream_data),
    (r"winktv\.co\.kr", "winktv", spider.get_winktv_stream_data),
    (r"popkontv\.com", "popkontv", spider.get_popkontv_stream_url),
    (r"twitcasting\.tv", "twitcasting", spider.get_twitcasting_stream_url),
    (r"weibo\.com", "weibo", spider.get_weibo_stream_data),
    (r"kugou\.com|fanxing", "kugou", spider.get_kugou_stream_url),
    (r"liveme\.com", "liveme", spider.get_liveme_stream_url),
    (r"huajiao\.com", "huajiao", spider.get_huajiao_stream_url),
    (r"zhihu\.com", "zhihu", spider.get_zhihu_stream_url),
    (r"baidu\.com", "baidu", spider.get_baidu_stream_data),
]


def detect_platform(url: str) -> tuple[str, PlatformFunc] | None:
    for pattern, name, func in PLATFORM_MAP:
        if re.search(pattern, url):
            return name, func
    return None


def _has_direct_play_url(d: dict) -> bool:
    return bool(
        d.get("m3u8_url")
        or d.get("flv_url")
        or d.get("record_url")
        or d.get("live_url")
        or d.get("play_url")
    )


def _douyin_nested_has_url(d: dict) -> bool:
    ss = d.get("stream_url")
    if not isinstance(ss, dict):
        return False
    hls = ss.get("hls_pull_url_map") or {}
    flv = ss.get("flv_pull_url") or {}
    return bool(hls or flv)


def _douyu_apply_h5_payload(data: dict, payload: dict) -> bool:
    if not isinstance(payload, dict):
        return False
    rtmp_url = (payload.get("rtmp_url") or "").strip()
    rtmp_live = (payload.get("rtmp_live") or "").strip()
    if rtmp_live:
        if rtmp_url:
            data["flv_url"] = f"{rtmp_url.rstrip('/')}/{rtmp_live.lstrip('/')}"
        else:
            data["flv_url"] = str(rtmp_live)
        return True
    for key in ("url", "hls_url", "live_url", "video_url", "rtmp_url"):
        u = payload.get(key)
        if isinstance(u, str) and u.strip().startswith("http"):
            data["flv_url"] = u.strip()
            return True
    multiline = payload.get("multiline")
    if isinstance(multiline, list) and multiline:
        first = multiline[0]
        if isinstance(first, dict):
            return _douyu_apply_h5_payload(data, first)
    return False


def _douyu_error_code(flv_json: dict) -> int | str | None:
    err = flv_json.get("error")
    if err is None:
        return 0
    return err


def _douyu_is_ok_error(err: int | str | None) -> bool:
    return err in (0, "0", None)


async def _enrich_playable_url(data: dict) -> None:
    """Douyu returns room info without FLV; fetch play URL (DLR stream helper + H5 API, multi-rate)."""
    if _has_direct_play_url(data) or _douyin_nested_has_url(data):
        return
    if data.get("_platform") != "douyu":
        return
    if not data.get("is_live"):
        return
    rid = str(data.get("room_id", "")).strip()
    if not rid:
        return

    cookies = get_douyu_cookies() or ""
    ck = get_douyu_cookies()
    _scope = douyu_token.douyu_fetch_cookies_scope(ck)
    try:
        await _enrich_playable_url_inner(data, rid, cookies)
    finally:
        douyu_token.douyu_fetch_cookies_reset(_scope)


async def _enrich_playable_url_inner(data: dict, rid: str, cookies: str) -> None:
    ck = get_douyu_cookies()
    for quality in ("OD", "HD", "SD"):
        work = {
            "is_live": True,
            "room_id": rid,
            "anchor_name": data.get("anchor_name") or "",
            "title": data.get("title") or "",
        }
        try:
            out = await dlr_stream.get_douyu_stream_url(
                work,
                video_quality=quality,
                cookies=cookies,
                proxy_addr=None,
            )
            if isinstance(out, dict) and out.get("flv_url"):
                data["flv_url"] = out["flv_url"]
                data["record_url"] = out.get("record_url") or out["flv_url"]
                return
        except Exception as exc:
            data["_douyu_last_msg"] = f"get_douyu_stream_url({quality}): {exc!s}"[:300]

    for rate in ("0", "-1", "2", "3", "1"):
        try:
            flv_json = await spider.get_douyu_stream_data(
                rid, rate=rate, proxy_addr=None, cookies=ck if ck else None
            )
            if not isinstance(flv_json, dict):
                data["_douyu_last_msg"] = f"rate={rate}: non-dict response"
                continue
            payload = flv_json.get("data")
            if isinstance(payload, str) and payload.strip().startswith("http"):
                data["flv_url"] = payload.strip()
                return
            pdict = payload if isinstance(payload, dict) else {}
            if _douyu_apply_h5_payload(data, pdict):
                return
            err = _douyu_error_code(flv_json)
            if not _douyu_is_ok_error(err):
                msg = flv_json.get("msg") or flv_json.get("message") or str(flv_json)[:200]
                data["_douyu_last_msg"] = f"error={err} rate={rate}: {msg}"
                continue
            if pdict and not data.get("flv_url"):
                data["_douyu_last_msg"] = (
                    f"rate={rate}: error ok but no rtmp fields in data keys={list(pdict.keys())[:8]}"
                )
        except Exception as exc:
            data["_douyu_last_msg"] = f"rate={rate} exception: {exc!s}"[:300]
            continue


async def parse_stream(url: str) -> dict:
    """Parse a live-room URL and return raw stream data from DouyinLiveRecorder."""
    result = detect_platform(url)
    if result is None:
        raise ValueError(f"Unsupported platform URL: {url}")
    platform_name, func = result
    raw = await func(url)
    data = normalize_spider_result(raw)
    data["_platform"] = platform_name
    data["_room_url"] = url
    await _enrich_playable_url(data)
    return data
