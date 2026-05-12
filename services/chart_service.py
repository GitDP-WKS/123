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
            lambda x: self._wrap_text(x, width=14)
        )

        figure = px.bar(
            chart_df,
            x='Тематика',
            y='Количество',
            color='Подрядчик',
            barmode='group',
            color_discrete_map={
                'NSP': '#0B5FFF',
                'E-Prom': '#111827',
                'Прочие': '#94A3B8'
            }
        )

        figure.update_layout(
            template='plotly_white',
            height=430,
            margin=dict(l=20, r=20, t=50, b=100),
            legend_title='Подрядчик',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='Segoe UI',
                size=12,
                color='#111827'
            )
        )

        figure.update_xaxes(
            tickangle=0,
            showgrid=False
        )

        figure.update_yaxes(
            gridcolor='#E5E7EB'
        )

        return figure

    def build_top5_chart(self, df: pd.DataFrame):

        chart_df = df.copy()

        chart_df['ЭЗС'] = chart_df['ЭЗС'].apply(
            lambda x: self._wrap_text(x, width=28)
        )

        figure = px.bar(
            chart_df,
            x='Количество',
            y='ЭЗС',
            orientation='h',
            color='Количество',
            color_continuous_scale=['#DCEBFF', '#0B5FFF']
        )

        figure.update_layout(
            template='plotly_white',
            height=430,
            margin=dict(l=20, r=20, t=50, b=20),
            yaxis={'categoryorder': 'total ascending'},
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
            gridcolor='#E5E7EB'
        )

        figure.update_yaxes(
            showgrid=False
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
                name='Обращения',
                marker_color='#0B5FFF'
            )
        )

        figure.add_trace(
            go.Scatter(
                x=df['Дата'],
                y=[sessions for _ in range(len(df))],
                mode='lines+markers',
                name='Сессии',
                line=dict(
                    color='#111827',
                    width=3
                )
            )
        )

        figure.update_layout(
            template='plotly_white',
            height=430,
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='Segoe UI',
                size=12,
                color='#111827'
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        figure.update_xaxes(
            showgrid=False
        )

        figure.update_yaxes(
            gridcolor='#E5E7EB'
        )

        return figure
