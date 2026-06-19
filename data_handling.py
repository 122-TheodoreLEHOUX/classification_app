import pandas as pd
from request_db import db_connection


class data_handler:
    def __init__(self, conn: db_connection):
        self.connection = conn

    def load(self) -> pd.DataFrame:
        """Load the full table from the backend as a DataFrame."""
        return self.connection.get_data()

    def update(self, df: pd.DataFrame) -> None:
        """Update/insert rows from the provided DataFrame into the backend."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")

        # Ensure columns are valid for DB
        if not self.connection.assert_columns(df):
            # allow extra columns but only keep known ones
            df = df.reindex(columns=self.connection.columns)

        self.connection.update_data(df)