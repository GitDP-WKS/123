from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches
from loguru import logger


EXPORTS_DIR = Path('data/exports')
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


class PPTService:
    """Production PPTX rendering engine."""

    def generate_presentation(
        self,
        period_label: str,
        total_calls: int,
        sessions: int,
        kwt: int
    ) -> str:

        presentation = Presentation()

        presentation.slide_width = Inches(13.33)
        presentation.slide_height = Inches(7.5)

        slide_layout = presentation.slide_layouts[6]
        slide = presentation.slides.add_slide(slide_layout)

        title_box = slide.shapes.add_textbox(
            Inches(0.4),
            Inches(0.2),
            Inches(12),
            Inches(0.6)
        )

        title_frame = title_box.text_frame

        title_frame.text = (
            'ДИНАМИКА ОБРАЩЕНИЙ ПОТРЕБИТЕЛЕЙ '
            f'ПО ЭЗС ЗА {period_label}'
        )

        metrics_box = slide.shapes.add_textbox(
            Inches(0.4),
            Inches(1.0),
            Inches(6),
            Inches(2)
        )

        metrics_frame = metrics_box.text_frame

        metrics_frame.text = (
            f'Обращений: {total_calls}\n'
            f'Сессии: {sessions}\n'
            f'кВт: {kwt}'
        )

        generated_at = datetime.now().strftime('%Y%m%d_%H%M%S')

        output_path = (
            EXPORTS_DIR /
            f'ev_charging_report_{generated_at}.pptx'
        )

        presentation.save(output_path)

        logger.info(
            'Presentation exported successfully: {}',
            output_path
        )

        return str(output_path)
