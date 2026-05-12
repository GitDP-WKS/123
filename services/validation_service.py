from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd
from loguru import logger


REQUIRED_COLUMNS = [
    'Дата',
    'Тематика',
    'ЭЗС',
    'Подрядчик'
]


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class ValidationService:
    """Production-safe validation layer for source data."""

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        try:
            df.columns = [str(col).strip() for col in df.columns]

            missing_columns = [
                col for col in REQUIRED_COLUMNS
                if col not in df.columns
            ]

            if missing_columns:
                errors.append(
                    f'Missing required columns: {missing_columns}'
                )

            if 'Дата' in df.columns:
                try:
                    df['Дата'] = pd.to_datetime(
                        df['Дата'],
                        errors='coerce'
                    )

                    invalid_dates = df['Дата'].isna().sum()

                    if invalid_dates > 0:
                        warnings.append(
                            f'Invalid dates detected: {invalid_dates}'
                        )

                except Exception as error:
                    logger.exception(error)
                    errors.append('Date parsing failed')

            duplicate_rows = df.duplicated().sum()

            if duplicate_rows > 0:
                warnings.append(
                    f'Duplicate rows detected: {duplicate_rows}'
                )

            if df.empty:
                errors.append('Source dataframe is empty')

        except Exception as error:
            logger.exception(error)
            errors.append(str(error))

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
