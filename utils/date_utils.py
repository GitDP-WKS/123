from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
from loguru import logger


DATE_FORMATS = [
    '%d.%m.%Y',
    '%d.%m.%y',
    '%d/%m/%Y',
    '%d/%m/%y',
    '%d-%m-%Y',
    '%d-%m-%y',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%d.%m.%Y %H:%M:%S',
    '%d.%m.%Y %H:%M',
    '%d/%m/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M',
]


def parse_single_date(value: Any) -> pd.Timestamp | pd.NaT:
    """Parse one Google Sheets date value safely.

    Supports:
    - dd.mm.yyyy / dd.mm.yy
    - dd/mm/yyyy / dd-mm-yyyy
    - yyyy-mm-dd
    - datetime strings with time
    - Google/Excel serial dates
    """

    if value is None or pd.isna(value):
        return pd.NaT

    raw = str(value).strip()

    if not raw:
        return pd.NaT

    raw = (
        raw.replace('\u00a0', ' ')
        .replace(',', '.')
        .replace('г.', '')
        .replace('г', '')
        .strip()
    )

    # Excel / Google Sheets serial date, for example 45778
    try:
        numeric_value = float(raw)
        if 30000 <= numeric_value <= 60000:
            return pd.to_datetime(
                numeric_value,
                unit='D',
                origin='1899-12-30',
                errors='coerce'
            )
    except Exception:
        pass

    for date_format in DATE_FORMATS:
        try:
            return pd.Timestamp(datetime.strptime(raw, date_format))
        except ValueError:
            continue

    parsed = pd.to_datetime(raw, errors='coerce', dayfirst=True)

    if pd.isna(parsed):
        logger.debug('Unparsed date value: {}', value)
        return pd.NaT

    return parsed


def parse_date_series(series: pd.Series) -> pd.Series:
    return series.apply(parse_single_date)
