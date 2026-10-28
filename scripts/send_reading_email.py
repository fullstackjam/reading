"""Email a newly published reading list through Resend."""

import argparse
import hashlib
import html
import json
import os
import re
from pathlib import Path

import httpx
import markdown

from src.ai.markdown_utils import clean_app_summary_markdown


SITE_URL = "https://reading.fullstackjam.com"
SENDER_NAME = "Jam's Reading List"
EMPTY_MARKER = "但没有达到重要性阈值的条目。"


def latest_summary(directory: Path) -> Path | None:
    summaries = sorted(
        path for path in directory.glob("horizon-*-zh.md")
        if re.fullmatch(r"horizon-\d{4}-\d{2}-\d{2}-zh\.md", path.name)
    )
    return summaries[-1] if summaries else None


def email_payload(summary: Path, recipient: str, sender: str) -> dict:
    date = summary.name.removeprefix("horizon-").removesuffix("-zh.md")
    content = summary.read_text(encoding="utf-8")
    content = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", content, count=1, flags=re.DOTALL)
    content = clean_app_summary_markdown(content)
    link = f"{SITE_URL}/archive/{date}.html"
    text = f"{content.strip()}\n\n查看本期清单：{link}\n"
    body = markdown.markdown(html.escape(content), extensions=["extra", "sane_lists"])
    return {
        "from": f"{SENDER_NAME} <{sender}>",
        "to": [recipient],
        "subject": f"本期值得读 · {date}",
        "text": text,
        "html": (
            '<html lang="zh-CN"><body style="font-family:sans-serif;line-height:1.7;'
            'max-width:720px;margin:0 auto;padding:24px">'
            f'{body}<hr><p><a href="{link}">查看本期清单与往期归档</a></p>'
            "</body></html>"
        ),
    }


def send_reading_email(
    summaries: Path,
    history: Path,
    *,
    recipient: str,
    sender: str,
    api_key: str,
    preview: Path | None = None,
) -> str:
    summary = latest_summary(summaries)
    if summary is None or EMPTY_MARKER in summary.read_text(encoding="utf-8"):
        return "No reading list to send"
    previous = history / summary.name
    if preview is None and previous.exists() and previous.read_bytes() == summary.read_bytes():
        return "No new reading list; email skipped"
    payload = email_payload(summary, recipient, sender)
    if preview is not None:
        preview.write_text(payload["html"], encoding="utf-8")
        return f"Email preview written to {preview}; no email sent"
    if not api_key or not recipient or not sender:
        raise ValueError("RESEND_API_KEY, READING_EMAIL_TO and READING_EMAIL_FROM are required")
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    response = httpx.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Idempotency-Key": f"reading/{fingerprint}",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    message_id = response.json()["id"]
    return f"Reading email accepted by Resend: {message_id}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summaries", type=Path, default=Path("public/summaries"))
    parser.add_argument("--history", type=Path, default=Path(".reading-history/summaries"))
    parser.add_argument("--preview", type=Path, help="Write HTML without sending an email")
    args = parser.parse_args()
    print(send_reading_email(
        args.summaries,
        args.history,
        recipient=os.environ.get("READING_EMAIL_TO", ""),
        sender=os.environ.get("READING_EMAIL_FROM", ""),
        api_key=os.environ.get("RESEND_API_KEY", ""),
        preview=args.preview,
    ))


if __name__ == "__main__":
    main()
