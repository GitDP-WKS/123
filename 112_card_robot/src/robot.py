from __future__ import annotations

import logging
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

from .event_log import setup_logging, write_event
from .notifier import notify
from .settings import Settings, load_settings

SCREENSHOT_DIR = Path("screenshots")


class CardRobot:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.recovery_attempts = 0

    def make_screenshot(self, page: Page, prefix: str) -> str:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        filename = SCREENSHOT_DIR / f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=str(filename), full_page=True)
        return str(filename)

    def open_cards_page(self, page: Page) -> None:
        logging.info("Открываю страницу карточек")
        page.goto(
            self.settings.cards_url,
            wait_until="domcontentloaded",
            timeout=self.settings.page_load_timeout_ms,
        )
        page.wait_for_timeout(1000)

    def login_if_needed(self, page: Page) -> bool:
        password_field = page.locator(self.settings.password_selector)
        if password_field.count() == 0:
            return False

        logging.info("Обнаружена страница авторизации. Выполняю вход")
        write_event("login", result="start")

        page.locator(self.settings.login_selector).first.fill(self.settings.login, timeout=self.settings.action_timeout_ms)
        password_field.first.fill(self.settings.password, timeout=self.settings.action_timeout_ms)
        page.locator(self.settings.submit_selector).first.click(timeout=self.settings.action_timeout_ms)
        page.wait_for_load_state("domcontentloaded", timeout=self.settings.page_load_timeout_ms)
        page.wait_for_timeout(1500)

        write_event("login", result="done")
        return True

    def get_new_cards_count(self, page: Page) -> int:
        return page.locator(self.settings.new_cards_selector).count()

    def accept_first_card(self, page: Page) -> bool:
        cards = page.locator(self.settings.new_cards_selector)
        count = cards.count()
        if count == 0:
            return False

        card = cards.first
        card_text = ""
        try:
            card_text = card.inner_text(timeout=self.settings.action_timeout_ms).strip()
        except Exception:
            card_text = "Текст карточки не считан"

        logging.info("Найдена карточка в первом столбце: %s", card_text.replace("\n", " "))
        write_event("card_detected", card_text=card_text, result="found")

        before_count = count
        card.click(timeout=self.settings.action_timeout_ms)
        page.wait_for_timeout(self.settings.after_click_wait_ms)

        after_count = self.get_new_cards_count(page)
        result = "clicked"
        details = f"before_count={before_count}; after_count={after_count}"

        logging.info("Карточка нажата. %s", details)
        write_event("card_clicked", card_text=card_text, result=result, details=details)
        return True

    def accept_cards_cycle(self, page: Page) -> None:
        accepted_in_cycle = 0

        while accepted_in_cycle < self.settings.max_cards_per_cycle:
            self.login_if_needed(page)
            count = self.get_new_cards_count(page)

            if count == 0:
                return

            self.accept_first_card(page)
            accepted_in_cycle += 1

        logging.warning("Достигнут лимит карточек за один цикл: %s", self.settings.max_cards_per_cycle)
        write_event("cycle_limit", result="warning", details=str(self.settings.max_cards_per_cycle))

    def recover(self, page: Page, reason: Exception) -> None:
        self.recovery_attempts += 1
        logging.exception("Ошибка робота. Попытка восстановления %s/%s", self.recovery_attempts, self.settings.max_recovery_attempts)
        write_event("error", result="recovery", details=str(reason))

        try:
            screenshot_path = self.make_screenshot(page, "error")
            logging.info("Скриншот ошибки: %s", screenshot_path)
        except Exception as screenshot_error:
            logging.warning("Не удалось сделать скриншот: %s", screenshot_error)

        if self.recovery_attempts >= self.settings.max_recovery_attempts:
            notify(
                self.settings,
                "Критическая ошибка робота 112. Не удалось восстановить работу после нескольких попыток. Нужна проверка рабочего места.",
            )
            self.recovery_attempts = 0
            time.sleep(10)

        try:
            page.reload(wait_until="domcontentloaded", timeout=self.settings.page_load_timeout_ms)
            page.wait_for_timeout(2000)
            self.login_if_needed(page)
            self.open_cards_page(page)
            write_event("recovery", result="page_reloaded")
        except Exception:
            page.goto(self.settings.site_url, wait_until="domcontentloaded", timeout=self.settings.page_load_timeout_ms)
            page.wait_for_timeout(2000)
            self.login_if_needed(page)
            self.open_cards_page(page)
            write_event("recovery", result="site_reopened")

    def run(self) -> None:
        setup_logging()
        logging.info("Запуск робота 112")
        write_event("robot", result="started")

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.settings.headless)
            context = browser.new_context(
                viewport={
                    "width": self.settings.viewport_width,
                    "height": self.settings.viewport_height,
                }
            )
            page = context.new_page()
            page.set_default_timeout(self.settings.action_timeout_ms)

            self.open_cards_page(page)

            while True:
                try:
                    self.login_if_needed(page)
                    self.accept_cards_cycle(page)
                    self.recovery_attempts = 0
                    time.sleep(self.settings.check_interval_sec)
                except PlaywrightTimeoutError as exc:
                    self.recover(page, exc)
                except Exception as exc:
                    self.recover(page, exc)


def main() -> None:
    settings = load_settings()
    CardRobot(settings).run()


if __name__ == "__main__":
    main()
