from __future__ import annotations

import json
from pathlib import Path
from typing import Any


LAYOUT_PATH = Path('config/layout.json')


class LayoutService:
    """Centralized layout configuration loader."""

    def load_layout(self) -> dict[str, Any]:

        if not LAYOUT_PATH.exists():
            raise FileNotFoundError('layout.json not found')

        with open(LAYOUT_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
