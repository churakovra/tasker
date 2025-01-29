import logging
import sqlite3
from datetime import datetime

from dotenv import dotenv_values

import config_reader


def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


sqlite3.register_adapter(datetime, adapt_datetime_iso)



def add_task(task: dict[str, str | int], user: dict[str, int | str]):
    with sqlite3.connect(config_reader.config.db_path.get_secret_value()) as con:
        cursor = con.cursor()
        task_val, date_to_do, user_id = task.values()
        task_values = [
            (task_val, date_to_do, datetime.now(), user_id)
        ]
        cursor.executemany(
            """
                insert into tasks_test
                (task, date_to_do, date_add, user_id)
                values
                (?, ?, ?, ?)
            """,
            task_values
        )
        user_id, username, fullname = user.values()
        user_values = [
            (user_id, username, fullname)
        ]
        try:
            cursor.executemany(
                """
                    insert into users_test
                    (user_id, username, fullname)
                    values
                    (?, ?, ?)
                """,
                user_values
            )
        except sqlite3.IntegrityError:
            print(f"Пользователь с id {user_id} уже существует")
        else:
            return
        con.commit()

def get_user_tasks(user_id: int) -> str:
    with sqlite3.connect(config_reader.config.db_path.get_secret_value()) as connection:
        cursor = connection.cursor()
        uid = (user_id,)
        tasks = [row[1] for row in cursor.execute('select * from tasks_test where user_id = ?', uid)]
        return ';\n'.join(tasks)