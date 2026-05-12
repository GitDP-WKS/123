from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd


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


EMPTY_VALUES = {
    '',
    'nan',
    'none',
    'null',
    '-',
    '--'
}


def parse_single_date(value: Any) -> pd.Timestamp | pd.NaT:

    if value is None or pd.isna(value):
        return pd.NaT

    if isinstance(value, pd.Timestamp):
        return value

    raw = str(value).strip()

    normalized = raw.lower().strip()

    if normalized in EMPTY_VALUES:
        return pd.NaT

    raw = (
        raw.replace('\u00a0', ' ')
        .replace(',', '.')
        .replace('г.', '')
        .replace('г', '')
        .replace('  ', ' ')
        .strip()
    )

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
            return pd.Timestamp(
                datetime.strptime(raw, date_format)
            )
        except ValueError:
            continue

    parsed = pd.to_datetime(
        raw,
        errors='coerce',
        dayfirst=True
    )

    return parsed


def parse_date_series(series: pd.Series) -> pd.Series:

    parsed_series = series.apply(parse_single_date)

    return parsed_series
