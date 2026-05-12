import streamlit as st
from loguru import logger

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

st.title('EV Charging Analytics Platform')
st.caption('Production-ready BI dashboard for automated PPTX generation')

with st.sidebar:
    st.header('Filters')

    period = st.selectbox(
        'Period',
        ['Week', 'Month', 'Custom']
    )

    st.divider()

    st.header('Manual Metrics')

    sessions = st.number_input(
        'Successful Sessions',
        min_value=0,
        value=7577
    )

    kwt = st.number_input(
        'kWh',
        min_value=0,
        value=153517
    )

st.info('Foundation architecture initialized successfully.')

col1, col2 = st.columns(2)

with col1:
    st.subheader('Topics Analytics')
    st.empty()

with col2:
    st.subheader('TOP-5 Stations')
    st.empty()

st.subheader('Dynamics')
st.empty()
