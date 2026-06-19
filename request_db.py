import sqlite3
import pandas as pd
from pathlib import Path
from typing import List


class db_connection:
    """Simple SQLite-backed connection for the classification app.

    Stores data in `data.db` in the project root and provides basic
    create/read/update helpers used by the Streamlit UI.
    """

    def __init__(self, db_path: str | Path = "data.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.table = "RepairReportTable"
        # Expected schema columns (from claude.md)
        self.columns: List[str] = [
            "OrderType",
            "operation_type",
            "Notification",
            "OS",
            "RmaNumber",
            "Reference",
            "Designation",
            "ReceiptDate",
            "SerialNumber",
            "Project",
            "ReturnNumber",
            "WorkCenter",
            "Location",
            "TypeOfWork",
            "SortingZone",
            "histo_location",
            "age_location",
            "CSContact",
            "lead_time",
            "RepairReport",
            "ClientFailureDescription",
            "FiClassifcation",
            "FailureType",
            "RepairStatus",
            "CompCardChanged",
            "Notes",
        ]

        self.create_table()

    def create_table(self) -> None:
        cols_sql = ", ".join([f"{c} TEXT" for c in self.columns])
        # Use Notification as primary key for upserts
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            {cols_sql},
            PRIMARY KEY (Notification)
        )
        """
        cur = self.conn.cursor()
        cur.execute(create_sql)
        self.conn.commit()

    def create_db(self) -> Path:
        # alias
        return self.db_path

    def update_data(self, df: pd.DataFrame) -> None:
        if df is None or df.empty:
            return

        # Ensure the frame has the expected columns (add missing ones)
        frame = df.copy()
        for c in self.columns:
            if c not in frame.columns:
                frame[c] = None

        cols = self.columns
        placeholders = ",".join(["?" for _ in cols])
        insert_sql = f"INSERT OR REPLACE INTO {self.table} ({','.join(cols)}) VALUES ({placeholders})"

        records = []
        for _, row in frame[cols].iterrows():
            values = [None if pd.isna(row[c]) else str(row[c]) for c in cols]
            records.append(values)

        cur = self.conn.cursor()
        cur.executemany(insert_sql, records)
        self.conn.commit()

    def get_data(self) -> pd.DataFrame:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {self.table}", self.conn)
        except Exception:
            # Table may not exist yet
            df = pd.DataFrame(columns=self.columns)
        return df

    def assert_columns(self, df: pd.DataFrame) -> bool:
        return set(df.columns).issubset(set(self.columns))