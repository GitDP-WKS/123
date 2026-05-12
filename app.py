from __future__ import annotations

import streamlit as st
from loguru import logger

from services.analytics_service import AnalyticsService
from services.chart_service import ChartService
from services.export_service import ExportService
from services.google_service import GoogleSheetsService
from services.history_service import HistoryService
from services.ppt_service import PPTService
from services.preview_service import PreviewService
from services.validation_service import ValidationService
from ui.styles import load_global_styles


st.set_page_config(
    page_title='EV Charging Analytics',
    layout='wide',
    initial_sidebar_state='expanded'
)

logger.add(
    'logs/app.log',
    rotation='10 MB',
    retention='30 days',
    level='INFO'
)

st.markdown(load_global_styles(), unsafe_allow_html=True)

st.title('ДИНАМИКА ОБРАЩЕНИЙ ПОТРЕБИТЕЛЕЙ ПО ЭЗС')
st.caption('Автоматическая аналитика Google Sheets → Preview → PPTX')

with st.sidebar:
    st.header('Параметры отчета')

    start_date = st.date_input(
        'Начало периода',
        value=None,
        format='DD.MM.YYYY'
    )

    end_date = st.date_input(
        'Конец периода',
        value=None,
        format='DD.MM.YYYY'
    )

    st.divider()

    st.header('Ручные показатели')

    sessions = st.number_input(
        'Успешные сессии',
        min_value=0,
        value=7577
    )

    kwt = st.number_input(
        'Количество кВт',
        min_value=0,
        value=153517
    )

    refresh = st.button('Обновить данные')


@st.cache_data(ttl=300, show_spinner='Загружаю данные из Google Sheets...')
def load_source_data():
    google_service = GoogleSheetsService()
    return google_service.load_data()


def normalize_source_columns(source_df):
    if len(source_df.columns) < 6:
        raise ValueError('В таблице меньше 6 колонок. Нужны B, D, E, F.')

    rename_mapping = {
        source_df.columns[1]: 'Дата',
        source_df.columns[3]: 'Тематика',
        source_df.columns[4]: 'ЭЗС',
        source_df.columns[5]: 'Подрядчик'
    }

    return source_df.rename(columns=rename_mapping)


try:
    if refresh:
        load_source_data.clear()

    validation_service = ValidationService()
    analytics_service = AnalyticsService()
    chart_service = ChartService()
    ppt_service = PPTService()
    export_service = ExportService()
    preview_service = PreviewService()
    history_service = HistoryService()

    source_df = normalize_source_columns(load_source_data())

    validation_result = validation_service.validate(source_df)

    for warning in validation_result.warnings:
        st.warning(warning)

    for error in validation_result.errors:
        st.error(error)

    if not validation_result.is_valid:
        st.stop()

    if not start_date or not end_date:
        st.info('Выберите начало и конец периода слева. Например: 04.05.2026 — 10.05.2026.')
        st.stop()

    if start_date > end_date:
        st.error('Начало периода не может быть позже конца периода.')
        st.stop()

    analytics = analytics_service.build_slide_analytics(
        df=source_df,
        start_date=str(start_date),
        end_date=str(end_date)
    )

    total_calls = int(analytics.topics_df['Количество'].sum()) if not analytics.topics_df.empty else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric('Обращений за период', total_calls)
    kpi2.metric('Успешные сессии', sessions)
    kpi3.metric('Количество кВт', kwt)

    if analytics.topics_df.empty:
        st.warning('За выбранный период обращений не найдено.')
        st.stop()

    topics_chart = chart_service.build_topics_chart(analytics.topics_df)
    top5_chart = chart_service.build_top5_chart(analytics.top5_df)
    dynamics_chart = chart_service.build_dynamics_chart(
        analytics.dynamics_df,
        sessions=sessions,
        kwt=kwt
    )

    st.divider()

    st.subheader('Preview будущего слайда')

    st.markdown(
        preview_service.render_slide_container(),
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Обращения по ЭЗС с разбивкой по тематикам')
        st.plotly_chart(topics_chart, use_container_width=True)

    with col2:
        st.markdown('### ТОП 5 станций за неделю')
        st.plotly_chart(top5_chart, use_container_width=True)

    st.markdown('### Количество принятых обращений')
    st.plotly_chart(dynamics_chart, use_container_width=True)

    st.divider()

    export_col1, export_col2 = st.columns([1, 2])

    with export_col1:
        generate_ppt = st.button(
            'Сгенерировать PPTX',
            use_container_width=True,
            type='primary'
        )

    if generate_ppt:

        topics_chart_path = export_service.export_chart_png(
            topics_chart,
            'topics_chart'
        )

        top5_chart_path = export_service.export_chart_png(
            top5_chart,
            'top5_chart'
        )

        dynamics_chart_path = export_service.export_chart_png(
            dynamics_chart,
            'dynamics_chart'
        )

        ppt_path = ppt_service.generate_presentation(
            period_label=analytics.period_label,
            total_calls=total_calls,
            sessions=sessions,
            kwt=kwt,
            topics_chart_path=topics_chart_path,
            top5_chart_path=top5_chart_path,
            dynamics_chart_path=dynamics_chart_path
        )

        history_service.save_export_record(
            period_label=analytics.period_label,
            total_calls=total_calls,
            sessions=sessions,
            kwt=kwt,
            ppt_path=ppt_path
        )

        with open(ppt_path, 'rb') as ppt_file:
            st.download_button(
                label='Скачать презентацию',
                data=ppt_file,
                file_name='ev_charging_report.pptx',
                mime='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                use_container_width=True
            )

        st.success('PPTX презентация успешно сгенерирована.')

    st.divider()

    st.subheader('История экспортов')

    recent_exports = history_service.get_recent_exports()

    if recent_exports:
        st.dataframe(recent_exports, use_container_width=True)
    else:
        st.info('История экспортов пока пуста.')

    with st.expander('Проверка данных'):
        st.write('TOP-5 станций')
        st.dataframe(analytics.top5_df, use_container_width=True)
        st.write('Тематики')
        st.dataframe(analytics.topics_df, use_container_width=True)
        st.write('Динамика')
        st.dataframe(analytics.dynamics_df, use_container_width=True)

except Exception as error:
    logger.exception(error)
    st.error('Ошибка при построении аналитики. Подробности записаны в logs/app.log')
