from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request

from .settings import Settings


def notify(settings: Settings, text: str) -> None:
    if not settings.telegram_enabled:
        return

    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        logging.warning("Telegram включен, но token/chat_id не заполнены")
        return

    try:
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": settings.telegram_chat_id,
            "text": text,
            "parse_mode": "HTML",
        }).encode("utf-8")

        request = urllib.request.Request(url, data=payload, method="POST")
        with urllib.request.urlopen(request, timeout=10) as response:
            json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        logging.warning("Не удалось отправить Telegram-уведомление: %s", exc)
