from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger


HISTORY_DIR = Path('data/history')
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_FILE = HISTORY_DIR / 'exports_history.json'


class HistoryService:
    """Tracks export history and report snapshots."""

    def save_export_record(
        self,
        period_label: str,
        total_calls: int,
        ppt_path: str
    ) -> None:

        history = self._load_history()

        history.append({
            'generated_at': datetime.now().isoformat(),
            'period': period_label,
            'total_calls': total_calls,
            'ppt_path': ppt_path
        })

        with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=2)

        logger.info('Export history updated.')

    def get_recent_exports(self) -> list[dict[str, Any]]:
        history = self._load_history()
        return sorted(
            history,
            key=lambda item: item['generated_at'],
            reverse=True
        )[:10]

    def _load_history(self) -> list[dict[str, Any]]:

        if not HISTORY_FILE.exists():
            return []

        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)

        except Exception as error:
            logger.exception(error)
            return []
