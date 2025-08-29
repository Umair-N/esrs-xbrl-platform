# taxonomy.py
from __future__ import annotations

import asyncio
import io
import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Dict, Iterator, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from api.dep import get_current_user, get_db
from fastapi import UploadFile, File
import shutil

from services.taxonomy_service import taxonomy_service
from psycopg2.extensions import connection as PGConnection
from api.dep import get_current_user, get_db 

# =========================
# Config (override via env)
# =========================
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../../config.json")
DEFAULT_TAXONOMY_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../output/taxonomy_outline.zip")
)

TAXONOMY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output/taxonomies"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE") or 64 * 1024)  # bytes per flush
MAX_CONCURRENT_STREAMS = int(os.getenv("MAX_CONCURRENT_STREAMS") or 3)
YIELD_EVERY_N_ITEMS = int(os.getenv("YIELD_EVERY_N_ITEMS") or 50)    # cooperative yield after N items
YIELD_INTERVAL_SEC = float(os.getenv("YIELD_INTERVAL_SEC") or 0.02)  # or every X seconds

# =========================
# Dependencies (stubs OK)
# =========================

taxonomy_router = APIRouter()
_stream_semaphore = asyncio.Semaphore(MAX_CONCURRENT_STREAMS)

# =========================
# Incremental JSON helpers
# =========================
def _iter_text_chunks(fileobj: io.BufferedReader, read_size: int) -> Iterator[str]:
    """Incrementally decode utf-8 bytes to text."""
    import codecs
    dec = codecs.getincrementaldecoder("utf-8")()
    while True:
        b = fileobj.read(read_size)
        if not b:
            break
        yield dec.decode(b)
    tail = dec.decode(b"", final=True)
    if tail:
        yield tail

def _is_array_start(sample: str) -> Optional[bool]:
    """Detect if first non-space char is '[' (array) or '{' (object)."""
    for ch in sample.lstrip():
        if ch == "[":
            return True
        if ch == "{":
            return False
        if ch:
            return False
    return None

def _parse_json_array(text_iter: Iterator[str]) -> Iterator[Any]:
    """
    Incrementally parse a huge JSON array (top-level or a sub-array) and yield items one by one.
    """
    decoder = json.JSONDecoder()
    buf = ""
    i = 0

    # seed until we have non-empty
    for chunk in text_iter:
        buf += chunk
        if buf.strip():
            break

    # find '['
    n = len(buf)
    while i < n and buf[i].isspace():
        i += 1
    if i >= n or buf[i] != "[":
        # Fallback: best-effort full parse (only used when not actually an array start)
        try:
            obj = json.loads(buf + "".join(text_iter))
            if isinstance(obj, list):
                for x in obj:
                    yield x
            else:
                yield obj
        except Exception:
            return
        return

    i += 1  # skip '['
    while True:
        n = len(buf)
        while i < n and (buf[i].isspace() or buf[i] == ","):
            i += 1
        while True:
            n = len(buf)
            if i >= n:
                try:
                    buf += next(text_iter)
                except StopIteration:
                    return
                continue
            if buf[i] == "]":
                return
            try:
                obj, end = decoder.raw_decode(buf, i)
                yield obj
                i = end
                break
            except json.JSONDecodeError:
                try:
                    buf += next(text_iter)
                except StopIteration:
                    return

def _parse_ndjson(text_iter: Iterator[str]) -> Iterator[Any]:
    """Parse NDJSON line-by-line; if a line isn't valid JSON, emit as {"value": "..."}."""
    carry = ""
    for chunk in text_iter:
        carry += chunk
        lines = carry.splitlines()
        if not carry.endswith(("\n", "\r\n")):
            carry = lines.pop() if lines else ""
        else:
            carry = ""
        for line in lines:
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except Exception:
                yield {"value": s}
    tail = carry.strip()
    if tail:
        try:
            yield json.loads(tail)
        except Exception:
            yield {"value": tail}

def _get_in(obj: Any, dotted: str, default=None):
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

def _match_filter(rec: Any, filter_key: Optional[str], filter_value: Optional[str]) -> bool:
    if filter_key is None or filter_value is None:
        return True
    v = _get_in(rec, filter_key, None)
    if v is None:
        return False
    s = str(v).lower()
    fv = str(filter_value).lower()
    if "*" in fv or "?" in fv:
        import fnmatch as _fn
        return _fn.fnmatch(s, fv)
    return fv in s

def _match_search(rec: Any, search_field: Optional[str], search_query: Optional[str]) -> bool:
    if not search_query:
        return True
    # treat None / "" / "*" / "any" as "search whole record (including children)"
    if search_field in (None, "", "*", "any"):
        return search_query.lower() in json.dumps(rec, ensure_ascii=False).lower()
    v = _get_in(rec, search_field, None)
    return search_query.lower() in str(v).lower() if v is not None else False

def _match_parent_level(rec: Any, parent_id: Optional[int], level: Optional[int]) -> bool:
    if parent_id is not None:
        pid = rec.get("parent_id") if isinstance(rec, dict) else None
        try:
            pid = int(pid) if pid is not None else None
        except Exception:
            pid = None
        if int(parent_id) == 0:
            if pid not in (0, None, "", -1):
                return False
        else:
            if pid != int(parent_id):
                return False
    if level is not None:
        lvl = rec.get("level") if isinstance(rec, dict) else None
        try:
            lvl = int(lvl) if lvl is not None else None
        except Exception:
            lvl = None
        if lvl != int(level):
            return False
    return True

def _apply_filters(
    rec: Any,
    filter_key: Optional[str],
    filter_value: Optional[str],
    search_query: Optional[str],
    search_field: Optional[str],
    parent_id: Optional[int],
    level: Optional[int],
    abstract_only: Optional[bool],
) -> bool:
    if abstract_only is True:
        if not (isinstance(rec, dict) and bool(rec.get("abstract"))):
            return False
    return (
        _match_filter(rec, filter_key, filter_value)
        and _match_search(rec, search_field, search_query)
        and _match_parent_level(rec, parent_id, level)
    )

# =========================
# Fast skipper for non-array values (prevents stalls)
# =========================
def _skip_json_value_fast(reader: io.BufferedReader, buf: str, i: int) -> tuple[str, int]:
    """
    Skip a single JSON value starting at buf[i] WITHOUT fully parsing it.
    Handles strings, objects, arrays, and primitives via scanning with balance/escape rules.
    Returns (buf, new_index).
    """
    def ensure(n: int = 1) -> bool:
        nonlocal buf
        if i + n <= len(buf):
            return True
        more = reader.read(65536)
        if not more:
            return False
        buf += more.decode("utf-8", errors="ignore")
        return True

    # skip leading whitespace
    while True:
        if not ensure():
            return buf, i
        if i < len(buf) and buf[i].isspace():
            i += 1
            continue
        break
    if i >= len(buf):
        return buf, i

    ch = buf[i]
    # 1) string
    if ch == '"':
        i += 1
        esc = False
        while True:
            if not ensure():
                return buf, i
            c = buf[i]
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                i += 1
                return buf, i
            i += 1

    # 2) object
    if ch == "{":
        i += 1
        depth = 1
        in_str = False
        esc = False
        while depth > 0:
            if not ensure():
                return buf, i
            c = buf[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
            i += 1
        return buf, i

    # 3) array
    if ch == "[":
        i += 1
        depth = 1
        in_str = False
        esc = False
        while depth > 0:
            if not ensure():
                return buf, i
            c = buf[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
            i += 1
        return buf, i

    # 4) primitive (number/true/false/null) -> read until a structural delimiter
    while True:
        if not ensure():
            return buf, i
        c = buf[i]
        if c in ",}]":
            return buf, i
        i += 1

# =========================
# Flattening item iterators
# =========================
def _iter_top_level_array_from_member(zf: zipfile.ZipFile, member: str, read_size: int) -> Iterator[Any]:
    """If the file's first non-space char is '[', parse it as a single array and yield items."""
    with zf.open(member, "r") as raw:
        reader = io.BufferedReader(raw, buffer_size=read_size)
        sample = reader.peek(min(4096, read_size)).decode("utf-8", errors="ignore")
        if _is_array_start(sample) is True:
            def text_iter():
                for s in _iter_text_chunks(reader, read_size=read_size):
                    yield s
            yield from _parse_json_array(text_iter())

def _iter_named_arrays_inline(zf: zipfile.ZipFile, member: str, read_size: int, names: List[str]) -> Iterator[Any]:
    """
    Find any "<name>: [ ... ]" arrays anywhere in the file and yield their items.
    Works for "concepts" and "valueAssertions" without losing trailing bytes.
    """
    pattern = re.compile(r'"(?:' + "|".join(map(re.escape, names)) + r')"\s*:', re.IGNORECASE)
    dec = json.JSONDecoder()
    with zf.open(member, "r") as raw:
        reader = io.BufferedReader(raw, buffer_size=max(65536, read_size))
        buf = ""
        while True:
            m = pattern.search(buf)
            if not m:
                more = reader.read(65536)
                if not more:
                    break
                # keep a small tail to handle tokens split across chunks
                if len(buf) > 2048:
                    buf = buf[-256:]
                buf += more.decode("utf-8", errors="ignore")
                continue

            i = m.end()
            # ws -> expect '['
            while True:
                if i >= len(buf):
                    more = reader.read(65536)
                    if not more:
                        return
                    buf += more.decode("utf-8", errors="ignore")
                    continue
                ch = buf[i]
                if ch.isspace():
                    i += 1
                    continue
                break

            if i >= len(buf) or buf[i] != "[":
                # Not an array value (unexpected) — skip past token and continue scanning
                buf = buf[i:]
                continue

            # Parse array inline, maintaining the same buffer
            i += 1  # after '['
            while True:
                # skip ws/commas
                while True:
                    if i >= len(buf):
                        more = reader.read(65536)
                        if not more:
                            return
                        buf += more.decode("utf-8", errors="ignore")
                        continue
                    ch = buf[i]
                    if ch.isspace() or ch == ",":
                        i += 1
                        continue
                    break

                if i >= len(buf):
                    more = reader.read(65536)
                    if not more:
                        return
                    buf += more.decode("utf-8", errors="ignore")
                    continue

                if buf[i] == "]":
                    # close array; drop everything up to here and continue scanning
                    i += 1
                    buf = buf[i:]
                    break

                # decode next item
                while True:
                    try:
                        item, end = dec.raw_decode(buf, i)
                        yield item
                        i = end
                        break
                    except json.JSONDecodeError:
                        more = reader.read(65536)
                        if not more:
                            return
                        buf += more.decode("utf-8", errors="ignore")

def _iter_top_level_value_arrays_from_member(zf: zipfile.ZipFile, member: str, read_size: int) -> Iterator[Any]:
    """
    Files shaped like:  { "200710": [ ... ], "301050": [ ... ], ... }
    Stream **every item** from **every** top-level array.
    Non-array values are skipped FAST (no full decode).
    """
    with zf.open(member, "r") as raw:
        reader = io.BufferedReader(raw, buffer_size=max(65536, read_size))
        buf = ""
        i = 0
        dec = json.JSONDecoder()

        def ensure(n: int = 1) -> bool:
            nonlocal buf
            if i + n <= len(buf):
                return True
            more = reader.read(65536)
            if not more:
                return False
            buf += more.decode("utf-8", errors="ignore")
            return True

        # seek first '{'
        while True:
            if not ensure():
                return
            ch = buf[i]
            if ch.isspace():
                i += 1
                continue
            if ch == "{":
                i += 1
                break
            # tolerate junk/BOM before '{'
            i += 1

        while True:
            # compact occasionally to keep memory bounded
            if i > 200_000:
                buf = buf[i:]
                i = 0

            # skip whitespace/commas
            while True:
                if not ensure():
                    return
                if i < len(buf) and (buf[i].isspace() or buf[i] == ","):
                    i += 1
                    continue
                break

            # end of top-level object?
            if i < len(buf) and buf[i] == "}":
                i += 1
                return

            # expect key string
            if not ensure():
                return
            if i >= len(buf) or buf[i] != '"':
                # be tolerant; advance a little and rescan
                i += 1
                continue

            # parse key quickly (small) using the decoder
            while True:
                try:
                    _, end = dec.raw_decode(buf, i)
                    break
                except json.JSONDecodeError:
                    if not ensure(65536):
                        return
            i = end

            # skip ws -> ':'
            while True:
                if not ensure():
                    return
                if i < len(buf) and buf[i].isspace():
                    i += 1
                    continue
                break
            if not ensure():
                return
            if i >= len(buf) or buf[i] != ":":
                i += 1
                continue
            i += 1  # after ':'

            # ws -> value
            while True:
                if not ensure():
                    return
                if i < len(buf) and buf[i].isspace():
                    i += 1
                    continue
                break
            if not ensure():
                return

            # CASE A: array value -> stream items inline
            if i < len(buf) and buf[i] == "[":
                i += 1
                while True:
                    # ws/commas
                    while True:
                        if not ensure():
                            return
                        if i < len(buf) and (buf[i].isspace() or buf[i] == ","):
                            i += 1
                            continue
                        break
                    if not ensure():
                        return
                    # end of array?
                    if i < len(buf) and buf[i] == "]":
                        i += 1
                        break
                    # decode one item
                    while True:
                        try:
                            item, end = dec.raw_decode(buf, i)
                            yield item
                            i = end
                            break
                        except json.JSONDecodeError:
                            if not ensure(65536):
                                return
                continue

            # CASE B: non-array value -> fast skip (no full parse)
            buf, i = _skip_json_value_fast(reader, buf, i)
            # next loop iteration handles delimiters

def _iter_flattened_items_from_member(zf: zipfile.ZipFile, member: str, read_size: int) -> Iterator[Any]:
    """
    Flatten strategy for ALL files:
      1) If top-level is an array: yield items from that array.
      2) Else yield items from ANY named arrays: "concepts" or "valueAssertions".
      3) Else flatten any top-level arrays that are values of the top-level object (e.g. "200511": [ ... ]).
    """
    yielded = False
    for item in _iter_top_level_array_from_member(zf, member, read_size):
        yielded = True
        yield item
    if yielded:
        return

    yielded = False
    for item in _iter_named_arrays_inline(zf, member, read_size, names=["concepts", "valueAssertions"]):
        yielded = True
        yield item
    if yielded:
        return

    for item in _iter_top_level_value_arrays_from_member(zf, member, read_size):
        yield item

# =========================
# Streaming engines
# =========================
async def _stream_raw_bytes(zip_path: str, member: str, chunk_bytes: int, rate_limit_bps: Optional[int]) -> AsyncIterator[bytes]:
    """Pass-through: stream the exact original file bytes in chunks."""
    async with _stream_semaphore:
        try:
            zf = zipfile.ZipFile(zip_path, "r")
        except FileNotFoundError:
            raise HTTPException(404, detail=f"ZIP not found: {zip_path}")
        except zipfile.BadZipFile:
            raise HTTPException(400, detail="Invalid ZIP file")
        try:
            if member not in zf.namelist():
                raise HTTPException(404, detail=f"Member '{member}' not found in ZIP")
            loop = asyncio.get_event_loop()
            window_start = loop.time()
            sent = 0
            with zf.open(member, "r") as f:
                while True:
                    chunk = f.read(chunk_bytes)
                    if not chunk:
                        break
                    if rate_limit_bps:
                        now = loop.time()
                        elapsed = max(now - window_start, 1e-6)
                        allowed = rate_limit_bps * elapsed
                        if sent + len(chunk) > allowed:
                            await asyncio.sleep((sent + len(chunk) - allowed) / rate_limit_bps)
                            window_start = loop.time()
                            sent = 0
                    yield chunk
                    sent += len(chunk)
                    # yield control so other requests can proceed
                    await asyncio.sleep(0)
        finally:
            try:
                zf.close()
            except Exception:
                pass

async def _stream_flattened(
    zip_path: str,
    member: str,
    chunk_bytes: int,
    rate_limit_bps: Optional[int],
    *,
    filter_key: Optional[str],
    filter_value: Optional[str],
    search_query: Optional[str],
    search_field: Optional[str],
    parent_id: Optional[int],
    level: Optional[int],
    abstract_only: Optional[bool],
    raw: bool,
) -> AsyncIterator[bytes]:
    """
    Streaming strategy:
      - raw=True: passthrough original file
      - no filters: single JSON array [ item, item, ... ]
      - with filters: NDJSON (one JSON per line)
    With cooperative yielding on every YIELD_EVERY_N_ITEMS or YIELD_INTERVAL_SEC.
    """
    if raw:
        async for b in _stream_raw_bytes(zip_path, member, chunk_bytes, rate_limit_bps):
            yield b
        return

    async with _stream_semaphore:
        out_buf = bytearray()
        loop = asyncio.get_event_loop()
        window_start = loop.time()
        sent = 0
        items_since_yield = 0
        last_yield = loop.time()

        def throttle(n: int) -> float:
            nonlocal window_start, sent
            if rate_limit_bps:
                now = loop.time()
                elapsed = max(now - window_start, 1e-6)
                allowed = rate_limit_bps * elapsed
                if sent + n > allowed:
                    return (sent + n - allowed) / rate_limit_bps
            return 0.0

        async def maybe_coop_yield():
            nonlocal items_since_yield, last_yield
            now = loop.time()
            if (items_since_yield >= YIELD_EVERY_N_ITEMS) or (now - last_yield >= YIELD_INTERVAL_SEC):
                items_since_yield = 0
                last_yield = now
                await asyncio.sleep(0)

        try:
            zf = zipfile.ZipFile(zip_path, "r")
        except FileNotFoundError:
            raise HTTPException(404, detail=f"ZIP not found: {zip_path}")
        except zipfile.BadZipFile:
            raise HTTPException(400, detail="Invalid ZIP file")

        try:
            if member not in zf.namelist():
                raise HTTPException(404, detail=f"Member '{member}' not found in ZIP")

            filters_used = any([
                filter_key is not None, filter_value is not None, search_query is not None,
                parent_id is not None, level is not None, abstract_only is not None
            ])

            try:
                if not filters_used:
                    # ---------- JSON array mode ----------
                    out_buf.extend(b"[")
                    delay = throttle(len(out_buf))
                    if delay:
                        await asyncio.sleep(delay)
                    yield bytes(out_buf)
                    sent += len(out_buf)
                    out_buf.clear()
                    first = True

                    for rec in _iter_flattened_items_from_member(zf, member, read_size=max(65536, chunk_bytes)):
                        if first:
                            first = False
                        else:
                            out_buf.extend(b",")

                        out_buf.extend(json.dumps(rec, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
                        items_since_yield += 1

                        if len(out_buf) >= chunk_bytes:
                            delay = throttle(len(out_buf))
                            if delay:
                                await asyncio.sleep(delay)
                            yield bytes(out_buf)
                            sent += len(out_buf)
                            out_buf.clear()
                            # even after a flush, yield control explicitly
                            await asyncio.sleep(0)
                            last_yield = loop.time()
                            items_since_yield = 0
                        else:
                            # no flush yet — still yield periodically
                            await maybe_coop_yield()

                    # close array
                    out_buf.extend(b"]")
                    delay = throttle(len(out_buf))
                    if delay:
                        await asyncio.sleep(delay)
                    yield bytes(out_buf)
                    sent += len(out_buf)
                    out_buf.clear()
                    await asyncio.sleep(0)

                else:
                    # ---------- NDJSON mode ----------
                    sep = b"\n"
                    for rec in _iter_flattened_items_from_member(zf, member, read_size=max(65536, chunk_bytes)):
                        if not _apply_filters(rec, filter_key, filter_value, search_query, search_field, parent_id, level, abstract_only):
                            continue
                        line = json.dumps(rec, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                        out_buf.extend(line)
                        out_buf.extend(sep)
                        items_since_yield += 1

                        if len(out_buf) >= chunk_bytes:
                            delay = throttle(len(out_buf))
                            if delay:
                                await asyncio.sleep(delay)
                            yield bytes(out_buf)
                            sent += len(out_buf)
                            out_buf.clear()
                            await asyncio.sleep(0)
                            last_yield = loop.time()
                            items_since_yield = 0
                        else:
                            await maybe_coop_yield()

                    if out_buf:
                        delay = throttle(len(out_buf))
                        if delay:
                            await asyncio.sleep(delay)
                        yield bytes(out_buf)
                        sent += len(out_buf)
                        out_buf.clear()
                        await asyncio.sleep(0)

            except asyncio.CancelledError:
                # Client disconnected: exit cleanly so semaphore releases
                return

        finally:
            try:
                zf.close()
            except Exception:
                pass

# =========================
# Response wrapper
# =========================
def _as_stream_response(
    gen,                   # AsyncIterator[bytes]
    content_type: str,     # e.g. "application/json; charset=utf-8"
    filename: str,         # suggested filename
    download: bool,        # add Content-Disposition to avoid Swagger/browser freezes
) -> StreamingResponse:
    headers = {
        "Cache-Control": "no-store",
        "X-Accel-Buffering": "no",
    }
    # When downloading, switch to octet-stream so Swagger doesn't try to render huge payloads
    if download:
        headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        media_type = "application/octet-stream"
    else:
        media_type = content_type
    return StreamingResponse(gen, media_type=media_type, headers=headers)

# =========================
# Endpoint factory
# =========================

def get_active_taxonomy() -> str:
    """Fetch the currently active taxonomy from config.json."""
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
            active_taxonomy_filename = config.get("active_taxonomy", "")
            if active_taxonomy_filename:
                # Construct the full path dynamically
                return os.path.join(TAXONOMY_DIR, active_taxonomy_filename)
    return ""  # Return empty string if no active taxonomy is set in config.json


def _make_flattened_handler(member_filename: str) -> Callable:
    async def handler(
        # search/filter
        filter_key: Optional[str] = Query(None, description="dot-notation key to filter"),
        filter_value: Optional[str] = Query(None, description="value to match; * and ? supported"),
        search_query: Optional[str] = Query(None, description="search term"),
        search_field: Optional[str] = Query("label", description='field to search: "label" (default) or "*" for full-record'),
        parent_id: Optional[int] = Query(None, description="parent_id filter (0 for roots)"),
        level: Optional[int] = Query(None, ge=0, description="level filter"),
        abstract_only: Optional[bool] = Query(None, description="only abstract items"),
        # streaming controls
        chunk_bytes: int = Query(CHUNK_SIZE, ge=4 * 1024, le=4 * 1024 * 1024, description="stream chunk size"),
        rate_limit_bps: Optional[int] = Query(None, ge=16 * 1024, description="optional throttle bytes/sec"),
        # Swagger/browser safety
        download: bool = Query(False, description="Force download to avoid rendering huge payloads"),
        # allow original bytes if needed
        raw: bool = Query(False, description="Return original file as-is (no flattening)"),
        # infra
        current_user=Depends(get_current_user),
        db=Depends(get_db),
    ):
        # ✅ derive user_id
        user_id = getattr(current_user, "id", None)
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")

        # ✅ resolve from DB via service
        zip_path = taxonomy_service.resolve_active_taxonomy_path(user_id=user_id, db=db)
        if not zip_path:
            raise HTTPException(status_code=404, detail="No active taxonomy available for this user.")

        # ✅ unchanged streaming call
        gen = _stream_flattened(
            zip_path, member_filename, chunk_bytes, rate_limit_bps,
            filter_key=filter_key, filter_value=filter_value,
            search_query=search_query, search_field=search_field,
            parent_id=parent_id, level=level, abstract_only=abstract_only,
            raw=raw,
        )

        filters_used = any([
            filter_key is not None, filter_value is not None, search_query is not None,
            parent_id is not None, level is not None, abstract_only is not None
        ])

        if raw:
            return _as_stream_response(gen, "application/json; charset=utf-8", member_filename, download)
        if filters_used:
            return _as_stream_response(
                gen,
                "application/x-ndjson; charset=utf-8",
                Path(member_filename).with_suffix(".ndjson").name,
                download,
            )
        else:
            nice = Path(member_filename).stem + "_flat.json"
            return _as_stream_response(gen, "application/json; charset=utf-8", nice, download)

    return handler

def register_streaming_endpoint(path: str, member_filename: str, *, name: str):
    handler = _make_flattened_handler(member_filename)
    taxonomy_router.add_api_route(
        path,
        handler,
        methods=["GET"],
        name=name,
        # unique operation id prevents Swagger duplicates
        operation_id=f"{name.replace(' ', '_')}_{path.strip('/').replace('/', '_')}",
    )

# =========================
# Routes (all flattened like presentations)
# =========================
ALIASES: Dict[str, List[str]] = {
    "taxonomy_outline.json": ["/taxonomy", "/taxonomy_outline"],
    "presentations.json":    ["/presentations", "/presentation"],
    "calculations.json":     ["/calculations", "/calculation"],
    "dimensions.json":       ["/dimensions", "/dimension"],
    "formulas.json":         ["/formulae", "/formulas", "/formula"],
    "concepts.json":         ["/concepts", "/concept"],
}

_registered_once = False
def _register_all_once():
    global _registered_once
    if _registered_once:
        return
    for member, paths in ALIASES.items():
        for p in paths:
            pretty = f"{Path(member).stem} [{p}]"
            register_streaming_endpoint(p, member, name=pretty)
    _registered_once = True

_register_all_once()




# def set_active_taxonomy(new_zip_path: str):
#     """Set the new active taxonomy by updating the config file."""
#     config = {"active_taxonomy": new_zip_path}
#     with open(CONFIG_FILE_PATH, "w") as f:
#         json.dump(config, f)


# # =========================
# # API to get the active taxonomy
# # =========================
# @taxonomy_router.get("/active")
# async def get_active_taxonomy_api():
#     """Returns the currently active taxonomy."""
#     active_taxonomy = get_active_taxonomy() 
#     if active_taxonomy:
#         return {"active_taxonomy": active_taxonomy}
#     else:
#         raise HTTPException(status_code=404, detail="No active taxonomy set.")

# =========================
# API to update/change the taxonomy (upload a new zip)
# =========================
# @taxonomy_router.post("/update")
# async def update_taxonomy(file: UploadFile = File(...)):
#     """Uploads a new taxonomy zip file and sets it as active."""
#     try:
#         # Define the path where the file will be stored
#         upload_dir = os.path.join(os.path.dirname(__file__), "../../../output/taxonomies")
#         os.makedirs(upload_dir, exist_ok=True)
#         zip_file_path = os.path.join(upload_dir, file.filename)

#         # Save the uploaded zip file
#         with open(zip_file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Set the new taxonomy as the active one
#         set_active_taxonomy(file.filename)

#         # Update the global variable for active taxonomy
#         global ACTIVE_TAXONOMY
#         ACTIVE_TAXONOMY = zip_file_path

#         return {"message": f"New taxonomy file '{file.filename}' is now active.", "file_path": zip_file_path}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to update taxonomy: {str(e)}")

# # =========================
# # API to disable the current taxonomy (set it to None)
# # =========================
# @taxonomy_router.post("/disable")
# async def disable_taxonomy():
#     """Disables the active taxonomy."""
#     global ACTIVE_TAXONOMY
#     ACTIVE_TAXONOMY = None
#     set_active_taxonomy("")  # Reset active taxonomy in config.json
#     return {"message": "Taxonomy has been disabled."}

# # =========================
# # API to get all available taxonomy files
# # =========================
# @taxonomy_router.get("/list")
# async def list_taxonomies():
#     """Returns the list of all taxonomy zip files in the 'output' directory."""
#     taxonomy_dir = os.path.join(os.path.dirname(__file__), "../../../output/taxonomies")
#     taxonomy_files = [f for f in os.listdir(taxonomy_dir) if f.endswith(".zip")]
#     return {"taxonomy_files": taxonomy_files}


# @taxonomy_router.post("/set-active")
# async def set_active_taxonomy_api(taxonomy_name: str = Query(..., description="The name of the taxonomy file to set as active")):
#     """Set an existing taxonomy file as the active one."""
    
#     TAXONOMY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output/taxonomies"))
#     taxonomy_path = os.path.join(TAXONOMY_DIR, taxonomy_name)

#     # Check if the specified file exists
#     if not os.path.exists(taxonomy_path):
#         raise HTTPException(status_code=404, detail=f"Taxonomy file '{taxonomy_name}' not found.")

#     # Set this taxonomy as the active one
#     set_active_taxonomy(taxonomy_name)

#     return {"message": f"Taxonomy '{taxonomy_name}' is now set as the active taxonomy."}