from io import StringIO

import pandas as pd

GOOGLE_SHEET_CSV_URL = (
    'https://docs.google.com/spreadsheets/d/'
    '1YN_8UtrZMqOTYZHaLzczwkkfocD-sS_wKrlSBmn-S50/'
    'export?format=csv&gid=426237753'
)


class GoogleSheetsService:
    """Service for loading Google Sheets data."""

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)

        df.columns = [str(col).strip() for col in df.columns]

        return df
