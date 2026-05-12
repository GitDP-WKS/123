from __future__ import annotations


def load_global_styles() -> str:
    return """
    <style>

    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1800px;
    }

    h1 {
        font-family: 'Segoe UI Semibold', sans-serif;
        font-size: 2.2rem;
        letter-spacing: -0.04em;
        color: #111827;
    }

    h2, h3 {
        font-family: 'Segoe UI Semibold', sans-serif;
        color: #111827;
    }

    .stMetric {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .stButton > button {
        border-radius: 12px;
        height: 46px;
        font-weight: 600;
    }

    section[data-testid='stSidebar'] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    div[data-testid='stPlotlyChart'] {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 10px;
    }

    </style>
    """
