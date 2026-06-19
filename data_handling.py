import pandas as pd
from request_db import db_connection

class data_handler():
    def __init__(self, conn : db_connection):
        self.connection = conn
        return 0
    
    def update(self, df : pd.DataFrame): 
        # update the dataframe in db based on df
        # key is OS
        return 0