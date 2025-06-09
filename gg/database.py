import os
import sqlite3
import importlib.resources as resources


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self.database = os.path.join(path, "gg.db")

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def create_database(self) -> None:
        with self._get_connection() as connection:
            with resources.open_text("gg", "database.sql") as sql:
                connection.executescript(sql.read())
            connection.commit()

    def create_sprint(self,
                      sprint_name: str,
                      base_commit_id: int | None) -> None:
        with self._get_connection() as connection:
            connection.execute("""
                               INSERT INTO SPRINT(NAME, BASE_COMMIT_ID)
                               VALUES (?, ?)""", (sprint_name, base_commit_id))
            connection.commit()
