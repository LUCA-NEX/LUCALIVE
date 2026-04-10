"""
Replace DouyinLiveRecorder's Douyu get_token_js: PC page HTML often no longer matches
the old regex (NoneType .group). Try mobile page + multiple patterns, with optional Cookie.

Upstream issue: https://github.com/ihmily/DouyinLiveRecorder/issues/1383
"""
from __future__ import annotations

import contextvars
import hashlib
import re
import time
from typing import List

import execjs

# get_douyu_stream_data does not pass cookies into get_token_js; we inject via context.
_cookie_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "lucalive_douyu_fetch_cookie", default=None
)


def douyu_fetch_cookies_scope(cookie: str | None):
    return _cookie_ctx.set(cookie)


def douyu_fetch_cookies_reset(token: contextvars.Token) -> None:
    _cookie_ctx.reset(token)


def _header_cookie() -> str | None:
    v = _cookie_ctx.get(None)
    if isinstance(v, str) and v.strip():
        return v.strip()
    return None


def _script_inners_with_ub(html: str) -> list[str]:
    """Prefer JS inside <script>…</script> so we never feed </script> from the document into Node."""
    out: list[str] = []
    for m in re.finditer(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", html, re.IGNORECASE):
        inner = m.group(1)
        if "ub98484234" in inner:
            out.append(inner)
    return out


def _sanitize_sign_blob(raw: str) -> str:
    """Regex often over-captures into the next HTML tag; Node then throws on </script>."""
    s = raw.strip()
    if s.startswith("<!--"):
        s = s[4:]
    if s.endswith("-->"):
        s = s[:-3]
    s = s.strip()
    low = s.lower()
    cut = len(s)
    for marker in ("</script>", "</style>"):
        i = low.find(marker)
        if i != -1:
            cut = min(cut, i)
    s = s[:cut].rstrip()
    # drop a trailing HTML tag fragment line
    lines = s.splitlines()
    while lines:
        t = lines[-1].strip().lower()
        if t.startswith("</") or t == ">" or t.startswith("<!"):
            lines.pop()
            continue
        break
    return "\n".join(lines).strip()


async def get_token_js(rid: str, did: str, proxy_addr: str | None = None) -> List[str]:
    from src.http_clients.async_http import async_req

    ck = _header_cookie()
    base_headers: dict[str, str] = {}
    if ck:
        base_headers["Cookie"] = ck

    attempts: list[tuple[str, dict[str, str], list[str]]] = [
        (
            f"https://www.douyu.com/{rid}",
            {
                **base_headers,
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
                "Referer": f"https://www.douyu.com/{rid}",
            },
            [
                r"(vdwdae325w_64we[\s\S]*function ub98484234[\s\S]*?)function",
                r"(function ub98484234\([\s\S]*?)(?=\r?\nfunction\s+[a-zA-Z_$][\w$]*\s*\()",
                r"(function ub98484234\([\s\S]*?)(?=\r?\n\s*var\s+[a-zA-Z_$][\w$]*\s*=)",
            ],
        ),
        (
            f"https://m.douyu.com/{rid}",
            {
                **base_headers,
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": f"https://m.douyu.com/{rid}",
            },
            [
                r"(vdwdae325w_64we[\s\S]*function ub98484234[\s\S]*?)function",
                r"(function ub98484234\([\s\S]*?)(?=\r?\nfunction\s+[a-zA-Z_$][\w$]*\s*\()",
                r"(function ub98484234\([\s\S]*?)\s*\r?\n\s*var\s+",
            ],
        ),
    ]

    html_str = ""
    result: str | None = None
    for url, headers, patterns in attempts:
        html_str = await async_req(url=url, proxy_addr=proxy_addr, headers=headers, http2=False)
        if not isinstance(html_str, str) or len(html_str) < 800:
            continue
        if "ub98484234" not in html_str:
            continue
        search_spaces = _script_inners_with_ub(html_str)
        if not search_spaces:
            search_spaces = [html_str]
        for space in search_spaces:
            for pat in patterns:
                m = re.search(pat, space)
                if m:
                    result = _sanitize_sign_blob(m.group(1))
                    break
            if result:
                break
        if result:
            break

    if not result:
        hint = "ub98484234"
        if isinstance(html_str, str) and hint not in html_str:
            hint = f"page has no {hint} (len={len(html_str)})"
        else:
            hint = "regex did not match sign block (Douyu HTML changed)"
        raise RuntimeError(
            f"douyu_sign_extract_failed: {hint}. "
            "Try updating DouyinLiveRecorder submodule or see github.com/ihmily/DouyinLiveRecorder/issues/1383"
        )

    func_ub9 = re.sub(r"eval.*?;}", "strc;}", result)
    func_ub9 = _sanitize_sign_blob(func_ub9)
    try:
        js = execjs.compile(func_ub9)
        res = js.call("ub98484234")
    except Exception as exc:
        if "</" in func_ub9[:2000] or "<script" in func_ub9.lower()[:2000]:
            raise RuntimeError(
                "douyu_sign_js_still_contains_html_after_sanitize; "
                "DouyinLiveRecorder issue #1383 — page layout may have changed."
            ) from exc
        raise RuntimeError(f"douyu_sign_execjs_ub98484234: {exc!s}") from exc

    if not isinstance(res, str):
        res = str(res)
    res = _sanitize_sign_blob(res)

    t10 = str(int(time.time()))
    vm = re.search(r"v=(\d+)", res)
    if not vm:
        raise RuntimeError("douyu_sign: no v= in ub98484234 output")
    v = vm.group(1)
    rb = hashlib.md5(f"{rid}{did}{t10}{v}".encode()).hexdigest()

    func_sign = re.sub(r"return rt;}\);?", "return rt;}", res)
    func_sign = func_sign.replace("(function (", "function sign(")
    func_sign = func_sign.replace("CryptoJS.MD5(cb).toString()", '"' + rb + '"')
    func_sign = _sanitize_sign_blob(func_sign)

    try:
        js = execjs.compile(func_sign)
        params = js.call("sign", rid, did, t10)
    except Exception as exc:
        raise RuntimeError(f"douyu_sign_execjs_sign: {exc!s}") from exc
    params_list = re.findall(r"=(.*?)(?=&|$)", params)
    if len(params_list) < 4:
        raise RuntimeError(f"douyu_sign: expected 4 params, got {len(params_list)}")
    return params_list


def patch_spider_get_token_js() -> None:
    import src.spider as sp

    sp.get_token_js = get_token_js
