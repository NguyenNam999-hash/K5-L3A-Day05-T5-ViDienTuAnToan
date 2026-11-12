#!/usr/bin/env python3
"""Local-only proxy for the T5 prototype.

The prototype is a static HTML file. This tiny server exists only to make one
real AI classification call at the main decision without ever putting the API
key in the HTML. If it is not running (or has no key), the prototype falls back
to a rule-based label and remains fully clickable.

Usage:
    python3 prototype/server.py
    open http://127.0.0.1:8765/?case=scam&step=handoff&ai=1

Reads the repo-root .env if present. Never prints or logs the key.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_PATH = ROOT / "ai-call-log.json"
ENV_PATH = ROOT.parent / ".env"

SYSTEM_PROMPT = """Bạn là bộ phân loại ý định cho trợ lý ví điện tử. Chỉ trả về JSON hợp lệ, không markdown, không giải thích ngoài JSON:
{"label":"bi_lua|khan_cap|chiem_tai_khoan|hoi_thong_tin","ly_do":"một câu ngắn"}

Quy ước:
- bi_lua: người dùng bị doạ, bị giục chuyển tiền gấp, bị yêu cầu "chứng minh trong sạch", có dấu hiệu bị lừa.
- khan_cap: người dùng đang ở tình huống gấp thật (quầy viện phí, quầy thanh toán), cần xử lý nhanh.
- chiem_tai_khoan: có dấu hiệu người khác chiếm tài khoản (máy lạ, đổi mật khẩu, người thân nhắn thay).
- hoi_thong_tin: hỏi thông tin chung, không gấp, không có dấu hiệu lừa.

Không tư vấn, không trả lời người dùng; chỉ phân loại."""

ALLOWED = {"bi_lua", "khan_cap", "chiem_tai_khoan", "hoi_thong_tin"}


def load_env() -> None:
    """Load simple `export KEY=value` lines without overriding real env vars."""
    if not ENV_PATH.exists():
        return
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def parse_json_object(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    match = re.search(r"\b(bi_lua|khan_cap|chiem_tai_khoan|hoi_thong_tin)\b", text)
    if match:
        return {"label": match.group(1), "ly_do": "Nhãn đọc từ câu trả lời."}
    return {"label": "hoi_thong_tin", "ly_do": "Không đọc được JSON; dùng nhãn an toàn."}


def append_log(entry: dict) -> None:
    try:
        if LOG_PATH.exists():
            data = json.loads(LOG_PATH.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        else:
            data = []
    except (OSError, json.JSONDecodeError):
        data = []
    data.append(entry)
    LOG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def classify(message: str, case: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    base = (os.environ.get("OPENAI_BASE_URL") or "").rstrip("/")
    model = os.environ.get("MODEL") or "deepseek-v4.1-flash"
    session = os.environ.get("OPENCODE_SESSION_ID")
    if not api_key or not base:
        raise RuntimeError("Thiếu OPENAI_API_KEY hoặc OPENAI_BASE_URL trong .env")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        "temperature": 0,
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # The gateway rejects Python-urllib's default signature (Cloudflare 1010).
        "User-Agent": "opencode-prototype/1.0",
    }
    if session:
        headers["x-opencode-session"] = session

    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"Model HTTP {exc.code}: {body}") from exc

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    parsed = parse_json_object(content)
    label = parsed.get("label") if parsed.get("label") in ALLOWED else "hoi_thong_tin"
    reason = str(parsed.get("ly_do") or "")[:300]

    usage = data.get("usage") or {}
    usage_slim = {k: usage.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens") if usage.get(k) is not None}
    entry = {
        "thoi_gian": datetime.now(timezone.utc).isoformat(),
        "case": case,
        "message": message,
        "label": label,
        "ly_do": reason,
        "model": data.get("model", model),
        "request_id": data.get("id"),
        "usage": usage_slim,
        "nguon": "ai_that",
    }
    append_log(entry)
    return {
        "label": label,
        "ly_do": reason,
        "model": entry["model"],
        "request_id": entry["request_id"],
        "usage": entry["usage"],
        "nguon": "ai_that",
    }


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?")[0] != "/api/classify":
            self.send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw.decode("utf-8") or "{}")
            message = str(body.get("message", "")).strip()[:2000]
            case = str(body.get("case", "")).strip()[:40]
            if not message:
                self.send_json(400, {"error": "message is required"})
                return
            self.send_json(200, classify(message, case))
        except Exception as exc:  # keep the prototype usable on any failure
            self.send_json(502, {"label": "khong_ro", "ly_do": "Không gọi được model.", "error": str(exc)[:240]})


def main() -> None:
    load_env()
    port = int(os.environ.get("PORT", "8765"))
    handler = partial(Handler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"Prototype: http://127.0.0.1:{port}/")
    print("Ctrl+C to stop. The API key stays in .env and is never sent to the browser.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    sys.exit(main())
