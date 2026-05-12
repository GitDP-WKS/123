from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class ChartService:
    """Unified chart rendering layer."""

    def build_topics_chart(self, df: pd.DataFrame):
        figure = px.bar(
            df,
            x='Тематика',
            y='Количество',
            color='Подрядчик',
            barmode='group'
        )

        figure.update_layout(
            template='plotly_white',
            height=420,
            margin=dict(l=20, r=20, t=40, b=120),
            legend_title='Подрядчик'
        )

        figure.update_xaxes(tickangle=-20)

        return figure

    def build_top5_chart(self, df: pd.DataFrame):
        figure = px.bar(
            df,
            x='Количество',
            y='ЭЗС',
            orientation='h'
        )

        figure.update_layout(
            template='plotly_white',
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis={'categoryorder': 'total ascending'}
        )

        return figure

    def build_dynamics_chart(
        self,
        df: pd.DataFrame,
        sessions: int,
        kwt: int
    ):
        figure = go.Figure()

        figure.add_trace(
            go.Bar(
                x=df['Дата'],
                y=df['Количество'],
                name='Обращения'
            )
        )

        figure.add_trace(
            go.Scatter(
                x=df['Дата'],
                y=[sessions for _ in range(len(df))],
                mode='lines+markers',
                name='Сессии'
            )
        )

        figure.update_layout(
            template='plotly_white',
            height=420,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        return figure
