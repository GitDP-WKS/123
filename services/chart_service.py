from __future__ import annotations

import textwrap
import pandas as pd
import plotly.graph_objects as go


class ChartService:

    @staticmethod
    def _wrap_text(value: str, width: int = 18) -> str:
        return '<br>'.join(textwrap.wrap(str(value), width=width))

    def build_topics_chart(self, df: pd.DataFrame):

        ordered_topics = [
            'Прочие вопросы без привязки к станции + Чат Бот',
            'в мобильном приложении ЭЗС не в сети',
            'самопроизвольное прерывание зарядной сессии',
            'станция недоступна (мониторинг КЦ)',
            'низкая скорость зарядки',
            'неисправность или загрязнение коннектора ЭЗС',
            'коннектор не извлекается из порта зарядки электромобиля',
            'мобильное приложение не запускает зарядную сессию'
        ]

        chart_df = df.copy()
        chart_df['Тематика'] = chart_df['Тематика'].astype(str).str.strip()

        grouped = (
            chart_df.groupby(['Тематика', 'Подрядчик'])
            .size()
            .reset_index(name='Количество')
        )

        figure = go.Figure()

        colors = {
            'E-Prom': '#BFBFBF',
            'NSP': '#0070C0',
            'Прочие': '#00B050'
        }

        for idx, topic in enumerate(reversed(ordered_topics)):

            topic_data = grouped[grouped['Тематика'] == topic]
            base_y = idx * 2

            for offset, contractor in enumerate(['E-Prom', 'NSP', 'Прочие']):

                row = topic_data[topic_data['Подрядчик'] == contractor]
                value = int(row['Количество'].iloc[0]) if not row.empty else 0

                if value <= 0:
                    continue

                figure.add_trace(
                    go.Bar(
                        x=[value],
                        y=[base_y + offset * 0.28],
                        orientation='h',
                        width=0.22,
                        marker_color=colors[contractor],
                        text=[value],
                        textposition='outside',
                        name=contractor,
                        showlegend=(idx == 0)
                    )
                )

        figure.update_layout(
            template='simple_white',
            height=720,
            margin=dict(l=430, r=120, t=30, b=80),
            paper_bgcolor='#F2F2F2',
            plot_bgcolor='#F2F2F2',
            font=dict(family='Segoe UI', size=15, color='#333333'),
            bargap=0.55,
            legend=dict(
                orientation='h',
                y=-0.12,
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(visible=False, range=[0, 20]),
            yaxis=dict(
                tickmode='array',
                tickvals=[i * 2 + 0.28 for i in range(len(ordered_topics))],
                ticktext=list(reversed(ordered_topics)),
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
