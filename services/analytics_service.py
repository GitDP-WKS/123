from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass
class SlideAnalytics:
    topics_df: pd.DataFrame
    top5_df: pd.DataFrame
    dynamics_df: pd.DataFrame
    period_label: str
    generated_at: datetime


class AnalyticsService:
    """Unified analytics engine for preview and PPT rendering."""

    def build_slide_analytics(
        self,
        df: pd.DataFrame,
        start_date: str,
        end_date: str
    ) -> SlideAnalytics:

        filtered_df = df.copy()

        filtered_df['Дата'] = pd.to_datetime(
            filtered_df['Дата'],
            errors='coerce'
        )

        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        filtered_df = filtered_df[
            (filtered_df['Дата'] >= start)
            &
            (filtered_df['Дата'] <= end)
        ]

        contractor_mapping = {
            'ЗЭТЗ': 'NSP',
            'E-Prom': 'E-Prom'
        }

        filtered_df['Подрядчик'] = (
            filtered_df['Подрядчик']
            .map(contractor_mapping)
            .fillna('Прочие')
        )

        topics_df = (
            filtered_df
            .groupby(['Тематика', 'Подрядчик'])
            .size()
            .reset_index(name='Количество')
            .sort_values('Количество', ascending=False)
        )

        top5_df = (
            filtered_df
            .groupby('ЭЗС')
            .size()
            .reset_index(name='Количество')
            .sort_values('Количество', ascending=False)
            .head(5)
        )

        dynamics_df = (
            filtered_df
            .groupby(filtered_df['Дата'].dt.date)
            .size()
            .reset_index(name='Количество')
        )

        return SlideAnalytics(
            topics_df=topics_df,
            top5_df=top5_df,
            dynamics_df=dynamics_df,
            period_label=f'{start_date} - {end_date}',
            generated_at=datetime.now()
        )
