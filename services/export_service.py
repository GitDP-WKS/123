from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
from loguru import logger


EXPORTS_DIR = Path('data/exports/charts')
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


class ExportService:
    """Service for exporting Plotly charts as PNG assets."""

    def export_chart_png(
        self,
        figure: go.Figure,
        filename: str,
        width: int = 1600,
        height: int = 900
    ) -> str:

        output_path = EXPORTS_DIR / f'{filename}.png'

        figure.write_image(
            str(output_path),
            width=width,
            height=height,
            scale=2
        )

        logger.info('Chart exported: {}', output_path)

        return str(output_path)
