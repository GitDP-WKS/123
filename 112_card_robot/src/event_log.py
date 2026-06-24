from __future__ import annotations

import csv
import logging
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
CSV_PATH = LOG_DIR / "events.csv"


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "robot.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    if not CSV_PATH.exists():
        with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([
                "datetime",
                "event_type",
                "card_text",
                "result",
                "details",
            ])


def write_event(event_type: str, card_text: str = "", result: str = "", details: str = "") -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("a", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            event_type,
            card_text.replace("\n", " ").strip(),
            result,
            details.replace("\n", " ").strip(),
        ])
