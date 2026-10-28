import httpx
import pytest

from scripts.send_reading_email import email_payload, send_reading_email


@pytest.fixture
def summaries(tmp_path):
    current = tmp_path / "current"
    history = tmp_path / "history"
    current.mkdir()
    history.mkdir()
    return current, history


def test_unchanged_or_empty_list_does_not_send(summaries, monkeypatch):
    current, history = summaries
    monkeypatch.setattr(httpx, "post", lambda *a, **kw: pytest.fail("Unexpected email"))
    assert send_reading_email(current, history, recipient="", api_key="") == "No reading list to send"
    name = "horizon-2026-10-28-zh.md"
    (current / name).write_text("# Reading\nAn article")
    (history / name).write_text("# Reading\nAn article")
    assert "skipped" in send_reading_email(current, history, recipient="", api_key="")
    (current / name).write_text("但没有达到重要性阈值的条目。")
    assert send_reading_email(current, history, recipient="", api_key="") == "No reading list to send"


def test_email_contains_readable_recommendations_and_archive_link(tmp_path):
    summary = tmp_path / "horizon-2026-10-28-zh.md"
    summary.write_text('---\nlang: zh\n---\n# 值得读\n\n[Article](https://example.com/a)\n\n推荐理由\n\n<img src=x onerror=alert(1)>')
    payload = email_payload(summary, "reader@example.com")
    assert payload["from"] == "Jam's Reading List <no-reply@fullstackjam.com>"
    assert payload["to"] == ["reader@example.com"]
    assert "2026-10-28" in payload["subject"]
    assert "推荐理由" in payload["text"]
    assert "lang: zh" not in payload["text"]
    assert '<a href="https://example.com/a">Article</a>' in payload["html"]
    assert "https://reading.fullstackjam.com/archive/2026-10-28.html" in payload["html"]
    assert "<img src=x" not in payload["html"]


def test_preview_needs_no_credentials_and_never_sends(summaries, tmp_path, monkeypatch):
    current, history = summaries
    (current / "horizon-2026-10-28-zh.md").write_text("# 值得读\n\n推荐理由")
    preview = tmp_path / "preview.html"
    monkeypatch.setattr(httpx, "post", lambda *a, **kw: pytest.fail("Unexpected email"))
    result = send_reading_email(current, history, recipient="", api_key="", preview=preview)
    assert "no email sent" in result
    assert "推荐理由" in preview.read_text()


def test_newest_list_sent_with_stable_idempotency_key(summaries, monkeypatch):
    current, history = summaries
    (current / "horizon-2026-10-27-zh.md").write_text("# Older")
    (current / "horizon-2026-10-28-zh.md").write_text("# Newer")
    requests = []

    def accept(url, **kwargs):
        requests.append(kwargs)
        return httpx.Response(200, json={"id": "test-message"}, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "post", accept)
    for _ in range(2):
        assert "test-message" in send_reading_email(current, history, recipient="reader@example.com", api_key="test-key")
    assert requests[0]["json"]["subject"] == "本期值得读 · 2026-10-28"
    assert requests[0]["headers"]["Idempotency-Key"] == requests[1]["headers"]["Idempotency-Key"]
    assert requests[0]["headers"]["Authorization"] == "Bearer test-key"


def test_missing_credentials_or_provider_failure_is_not_reported_as_success(summaries, monkeypatch):
    current, history = summaries
    (current / "horizon-2026-10-28-zh.md").write_text("# New")
    with pytest.raises(ValueError, match="required"):
        send_reading_email(current, history, recipient="reader@example.com", api_key="")

    def reject(url, **kwargs):
        return httpx.Response(403, json={"message": "Domain not verified"}, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "post", reject)
    with pytest.raises(httpx.HTTPStatusError):
        send_reading_email(current, history, recipient="reader@example.com", api_key="test-key")
