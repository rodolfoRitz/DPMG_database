import sqlite3
from sqlite3 import Cursor


class Database:
    def __init__(self, db_path: str) -> None:
        self.conx = sqlite3.connect(db_path)
    
    def get_all(self, query: str) -> list[tuple]:
        cursor = self.get_cursor()

        cursor.execute(query)
        data = cursor.fetchall()
        
        cursor.close()

        return data

    def execute(self, query: str, *params):
        try:
            cursor = self.get_cursor()
            cursor.execute(query, params)
            self.conx.commit()
        except:
            self.conx.rollback()
        finally:
            cursor.close()
        
    def get_cursor(self) -> Cursor:
        return self.conx.cursor()