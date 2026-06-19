import pandas as pd
from pathlib import Path

class db_connection():
    def __init__():
        return 0
    
    def create_db(self) -> Path:
        # create db if inexisting
        self.create_table()
        return 0

    def create_table(self) :
        # create table
        return 0
    
    def update_data(self, df : pd.DataFrame):
        # Compare df data to db and update goods rows
        return 0
    
    def get_data() -> pd.DataFrame :
        # return dataframe of data stock in 
        return 0
    
    def assert_columns(self, df : pd.DataFrame) -> bool:
        # Assert if columns have the same names as db
        return True