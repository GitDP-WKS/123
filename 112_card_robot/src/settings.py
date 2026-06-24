from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    site_url: str
    cards_url: str
    login: str
    password: str
    headless: bool
    viewport_width: int
    viewport_height: int
    check_interval_sec: float
    page_load_timeout_ms: int
    action_timeout_ms: int
    after_click_wait_ms: int
    max_cards_per_cycle: int
    max_recovery_attempts: int
    new_cards_selector: str
    login_selector: str
    password_selector: str
    submit_selector: str
    telegram_enabled: bool
    telegram_bot_token: str
    telegram_chat_id: str


def load_settings(config_path: str = "config.json") -> Settings:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Не найден файл настроек {config_path}. Скопируйте config.example.json в config.json и заполните параметры."
        )

    data = json.loads(path.read_text(encoding="utf-8"))

    required = ["site_url", "cards_url", "login", "password", "new_cards_selector"]
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"В config.json не заполнены обязательные поля: {', '.join(missing)}")

    return Settings(
        site_url=data["site_url"],
        cards_url=data["cards_url"],
        login=data["login"],
        password=data["password"],
        headless=bool(data.get("headless", False)),
        viewport_width=int(data.get("viewport_width", 1920)),
        viewport_height=int(data.get("viewport_height", 1080)),
        check_interval_sec=float(data.get("check_interval_sec", 2)),
        page_load_timeout_ms=int(data.get("page_load_timeout_ms", 30000)),
        action_timeout_ms=int(data.get("action_timeout_ms", 5000)),
        after_click_wait_ms=int(data.get("after_click_wait_ms", 1500)),
        max_cards_per_cycle=int(data.get("max_cards_per_cycle", 20)),
        max_recovery_attempts=int(data.get("max_recovery_attempts", 3)),
        new_cards_selector=data["new_cards_selector"],
        login_selector=data.get("login_selector", "input[type='text']"),
        password_selector=data.get("password_selector", "input[type='password']"),
        submit_selector=data.get("submit_selector", "button:has-text('Войти')"),
        telegram_enabled=bool(data.get("telegram_enabled", False)),
        telegram_bot_token=data.get("telegram_bot_token", ""),
        telegram_chat_id=data.get("telegram_chat_id", ""),
    )
