import os
import sqlite3
import importlib.resources as resources


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self.database = os.path.join(path, "gg.db")

    def create_database(self) -> None:
        with sqlite3.connect(self.database) as connection:
            with resources.open_text("gg", "database.sql") as sql:
                connection.executescript(sql.read())
            connection.commit()
