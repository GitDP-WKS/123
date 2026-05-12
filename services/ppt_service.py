from __future__ import annotations

from datetime import datetime
from pathlib import Path

from loguru import logger
from pptx import Presentation
from pptx.util import Inches


EXPORTS_DIR = Path('data/exports')
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


class PPTService:
    """Production PPTX rendering engine."""

    def generate_presentation(
        self,
        period_label: str,
        total_calls: int,
        sessions: int,
        kwt: int,
        topics_chart_path: str | None = None,
        top5_chart_path: str | None = None,
        dynamics_chart_path: str | None = None
    ) -> str:

        presentation = Presentation()

        presentation.slide_width = Inches(13.33)
        presentation.slide_height = Inches(7.5)

        slide_layout = presentation.slide_layouts[6]
        slide = presentation.slides.add_slide(slide_layout)

        title_box = slide.shapes.add_textbox(
            Inches(0.3),
            Inches(0.2),
            Inches(12.5),
            Inches(0.5)
        )

        title_frame = title_box.text_frame

        title_frame.text = (
            'ДИНАМИКА ОБРАЩЕНИЙ ПОТРЕБИТЕЛЕЙ '
            f'ПО ЭЗС ЗА {period_label}'
        )

        metrics_box = slide.shapes.add_textbox(
            Inches(0.3),
            Inches(0.75),
            Inches(6),
            Inches(0.4)
        )

        metrics_frame = metrics_box.text_frame

        metrics_frame.text = (
            f'Обращений: {total_calls}    '
            f'Сессии: {sessions}    '
            f'кВт: {kwt}'
        )

        if topics_chart_path:
            slide.shapes.add_picture(
                topics_chart_path,
                Inches(0.3),
                Inches(1.2),
                Inches(6.1),
                Inches(2.6)
            )

        if top5_chart_path:
            slide.shapes.add_picture(
                top5_chart_path,
                Inches(6.7),
                Inches(1.2),
                Inches(6.0),
                Inches(2.6)
            )

        if dynamics_chart_path:
            slide.shapes.add_picture(
                dynamics_chart_path,
                Inches(0.3),
                Inches(4.1),
                Inches(12.4),
                Inches(2.8)
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
