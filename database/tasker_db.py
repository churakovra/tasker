import sqlite3
from datetime import datetime

import config_reader


def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()


sqlite3.register_adapter(datetime, adapt_datetime_iso)
path = config_reader.config.db_path.get_secret_value()


def add_task(task: dict[str, str | int | datetime], user: dict[str, int | str | None]):
    with sqlite3.connect(path) as con:
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


def get_user_tasks(user_id: int) -> list[str]:
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()
        uid = [user_id, ]
        sql_query = """
        select 
                row_number() over (order by task_id) rn,
                task,
                date_to_do,
                date_add,
                user_id
            from tasks_test tt
            where user_id = ?
        """
        tasks = []
        for row in cursor.execute(sql_query, uid):
            cnt = row[0]
            task = row[1]
            date = datetime.fromisoformat(row[2]).strftime("%d.%m.%Y")
            tasks.append(f'{cnt}. {task} {date}')

        return tasks
