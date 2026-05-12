from __future__ import annotations

import textwrap
import pandas as pd
import plotly.graph_objects as go


class ChartService:

    @staticmethod
    def _wrap_text(value: str, width: int = 18) -> str:
        return '<br>'.join(textwrap.wrap(str(value), width=width))

    def build_topics_chart(self, df: pd.DataFrame):

        chart_df = df.copy()

        chart_df['Тематика'] = (
            chart_df['Тематика']
            .astype(str)
            .str.strip()
        )

        chart_df['Подрядчик'] = (
            chart_df['Подрядчик']
            .astype(str)
            .str.strip()
            .replace({
                'ЗЭТЗ': 'NSP',
                'NSP': 'NSP',
                'E-Prom': 'E-Prom',
                'Е-Пром': 'E-Prom'
            })
        )

        grouped = (
            chart_df.groupby(['Тематика', 'Подрядчик'])
            .size()
            .reset_index(name='Количество')
        )

        totals = (
            grouped.groupby('Тематика')['Количество']
            .sum()
            .reset_index()
            .sort_values('Количество', ascending=False)
        )

        topics = totals['Тематика'].tolist()

        other_topic = None

        for topic in topics:
            if 'прочие' in topic.lower():
                other_topic = topic
                break

        if other_topic:
            topics.remove(other_topic)
            topics.insert(0, other_topic)

        figure = go.Figure()

        colors = {
            'E-Prom': '#BFBFBF',
            'NSP': '#0070C0',
            'Прочие': '#00B050'
        }

        for idx, topic in enumerate(reversed(topics)):

            topic_data = grouped[grouped['Тематика'] == topic]
            base_y = idx * 2

            e_prom_value = 0
            nsp_value = 0

            e_prom_row = topic_data[
                topic_data['Подрядчик'] == 'E-Prom'
            ]

            if not e_prom_row.empty:
                e_prom_value = int(e_prom_row['Количество'].iloc[0])

            nsp_row = topic_data[
                topic_data['Подрядчик'] == 'NSP'
            ]

            if not nsp_row.empty:
                nsp_value = int(nsp_row['Количество'].iloc[0])

            if 'прочие' in topic.lower():

                total_other = e_prom_value + nsp_value

                figure.add_trace(
                    go.Bar(
                        x=[total_other],
                        y=[base_y],
                        orientation='h',
                        width=0.24,
                        marker_color=colors['Прочие'],
                        text=[total_other],
                        textposition='outside',
                        name='Прочие вопросы',
                        showlegend=(idx == 0)
                    )
                )

                continue

            if e_prom_value > 0:

                figure.add_trace(
                    go.Bar(
                        x=[e_prom_value],
                        y=[base_y],
                        orientation='h',
                        width=0.22,
                        marker_color=colors['E-Prom'],
                        text=[e_prom_value],
                        textposition='outside',
                        name='E-Prom',
                        showlegend=(idx == 0)
                    )
                )

            if nsp_value > 0:

                figure.add_trace(
                    go.Bar(
                        x=[nsp_value],
                        y=[base_y + 0.30],
                        orientation='h',
                        width=0.22,
                        marker_color=colors['NSP'],
                        text=[nsp_value],
                        textposition='outside',
                        name='NSP',
                        showlegend=(idx == 0)
                    )
                )

        figure.update_layout(
            template='simple_white',
            height=720,
            margin=dict(l=430, r=120, t=30, b=80),
            paper_bgcolor='#F2F2F2',
            plot_bgcolor='#F2F2F2',
            font=dict(
                family='Segoe UI',
                size=15,
                color='#333333'
            ),
            bargap=0.60,
            legend=dict(
                orientation='h',
                y=-0.12,
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                visible=False,
                range=[0, max(grouped['Количество'].max() + 5, 20)]
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[i * 2 + 0.15 for i in range(len(topics))],
                ticktext=list(reversed(topics)),
                showgrid=False
            )
        )

        return figure

    def build_top5_chart(self, df: pd.DataFrame):

        chart_df = df.copy()
        chart_df['ЭЗС'] = chart_df['ЭЗС'].apply(lambda x: self._wrap_text(x, width=16))

        figure = go.Figure()

        figure.add_bar(
            x=chart_df['ЭЗС'],
            y=chart_df['Количество'],
            text=chart_df['Количество'],
            textposition='outside',
            marker_color='#0070C0'
        )

        figure.update_layout(
            template='simple_white',
            height=430,
            margin=dict(l=20, r=20, t=40, b=100),
            paper_bgcolor='#F2F2F2',
            plot_bgcolor='#F2F2F2',
            showlegend=False
        )

        figure.update_xaxes(showgrid=False)
        figure.update_yaxes(showgrid=False)

        return figure

    def build_dynamics_chart(self):

        months = ['май.25','июн.25','июл.25','авг.25','сен.25','окт.25','ноя.25','дек.25','янв.26','фев.26','мар.26','апр.26','май.26']
        values = [191,272,290,249,220,238,243,257,246,221,211,237,95]

        colors = ['#5B84D7','#ED8B47','#B9B9B9','#F4C22B','#7FB2E5','#84B45F','#4C6796','#B56B33','#8A8A8A','#B29227','#4B79A6','#688C4E','#9DB2D9']

        figure = go.Figure()

        figure.add_bar(
            x=months,
            y=values,
            text=values,
            textposition='inside',
            marker_color=colors
        )

        figure.update_layout(
            template='simple_white',
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='#F2F2F2',
            plot_bgcolor='#F2F2F2',
            showlegend=False
        )

        figure.update_xaxes(showgrid=False)
        figure.update_yaxes(showgrid=False, visible=False)

        return figure
