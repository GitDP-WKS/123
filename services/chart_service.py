from __future__ import annotations

import textwrap

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class ChartService:
    """Unified chart rendering layer."""

    @staticmethod
    def _wrap_text(value: str, width: int = 18) -> str:
        return '<br>'.join(textwrap.wrap(str(value), width=width))

    def build_topics_chart(self, df: pd.DataFrame):

        chart_df = df.copy()

        chart_df['Тематика'] = chart_df['Тематика'].apply(
            lambda x: self._wrap_text(x, width=24)
        )

        figure = px.bar(
            chart_df,
            y='Тематика',
            x='Количество',
            color='Подрядчик',
            orientation='h',
            barmode='group',
            text='Количество',
            color_discrete_map={
                'NSP': '#0B5FFF',
                'E-Prom': '#111827',
                'Прочие': '#94A3B8'
            }
        )

        figure.update_traces(
            textposition='outside',
            cliponaxis=False
        )

        figure.update_layout(
            template='plotly_white',
            height=430,
            margin=dict(l=20, r=60, t=50, b=20),
            legend_title='Подрядчик',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='Segoe UI',
                size=12,
                color='#111827'
            )
        )

        figure.update_xaxes(gridcolor='#E5E7EB')
        figure.update_yaxes(showgrid=False)

        return figure

    def build_top5_chart(self, df: pd.DataFrame):

        chart_df = df.copy()

        chart_df['ЭЗС'] = chart_df['ЭЗС'].apply(
            lambda x: self._wrap_text(x, width=16)
        )

        figure = px.bar(
            chart_df,
            x='ЭЗС',
            y='Количество',
            text='Количество',
            color='Количество',
            color_continuous_scale=['#DCEBFF', '#0B5FFF']
        )

        figure.update_traces(
            textposition='outside',
            cliponaxis=False
        )

        figure.update_layout(
            template='plotly_white',
            height=430,
            margin=dict(l=20, r=20, t=50, b=90),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='Segoe UI',
                size=12,
                color='#111827'
            ),
            coloraxis_showscale=False
        )

        figure.update_xaxes(
            tickangle=0,
            showgrid=False
        )

        figure.update_yaxes(gridcolor='#E5E7EB')

        return figure

    def build_dynamics_chart(self):

        months = [
            'Май 2025', 'Июн 2025', 'Июл 2025', 'Авг 2025',
            'Сен 2025', 'Окт 2025', 'Ноя 2025', 'Дек 2025',
            'Янв 2026', 'Фев 2026', 'Мар 2026', 'Апр 2026', 'Май 2026'
        ]

        values = [120, 135, 128, 144, 151, 165, 170, 168, 180, 176, 184, 193, 205]

        colors = [
            '#0B5FFF', '#111827', '#16A34A', '#9333EA',
            '#EA580C', '#0891B2', '#DC2626', '#7C3AED',
            '#2563EB', '#059669', '#D97706', '#DB2777', '#0F172A'
        ]

        figure = go.Figure(
            data=[
                go.Bar(
                    x=months,
                    y=values,
                    text=values,
                    textposition='outside',
                    marker_color=colors
                )
            ]
        )

        figure.update_layout(
            template='plotly_white',
            height=430,
            margin=dict(l=20, r=20, t=50, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='Segoe UI',
                size=12,
                color='#111827'
            ),
            showlegend=False
        )

        figure.update_xaxes(showgrid=False)
        figure.update_yaxes(gridcolor='#E5E7EB')

        return figure
