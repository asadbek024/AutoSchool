import sqlite3 as sq
from config import patern
def connect():
    try:
        with sq.connect(patern.bot.db) as db:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    user_name TEXT,
                    state INTEGER,
                    score INTEGER,
                    true_answers TEXT,
                    message INTEGER,
                    group_id INTEGER
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions(
                    id INTEGER PRIMARY KEY,
                    topic INTEGER,
                    file_id TEXT,
                    question TEXT,
                    variants TEXT
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    topic INTEGER,
                    message INTEGER
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS marafon(
                    id INTEGER PRIMARY KEY,
                    file TEXT,
                    question TEXT,
                    answers TEXT
                )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topic(
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )""")
    except sq.Error as err:
        raise Exception(err)
def sqlite_decorate(func):
    def connect(values:list):
        try:
            with sq.connect(patern.bot.db) as db:
                data = func(db.cursor(), values)
                return data
        except Exception as err:
            print(f"{func.__name__} err: {err}")
            raise err
    return connect

@sqlite_decorate
def delete_group(cur:sq.Cursor, values:list) -> None:
    cur.execute("DELETE FROM groups WHERE id=?", values)

@sqlite_decorate
def delete_student(cur:sq.Cursor, values:list) -> None:
    cur.execute("DELETE FROM students WHERE id=?", values)

@sqlite_decorate
def update_true_answers(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE students SET true_answers=? WHERE id=?", values)

@sqlite_decorate
def get_true_answers(cur:sq.Cursor, values:list) -> str:
    return cur.execute("SELECT true_answers FROM students WHERE id=?", values).fetchone()[0]

@sqlite_decorate
def set_students(cur:sq.Cursor, values:list) -> None:
    cur.execute("INSERT INTO students(id, name, user_name, state, score, true_answers, message, group_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", values)

@sqlite_decorate
def get_students(cur:sq.Cursor, values:list) -> tuple:
    return cur.execute("SELECT name FROM students WHERE id=?", values).fetchone()

@sqlite_decorate
def check_student(cur:sq.Cursor, values:list) -> bool:
    if cur.execute("SELECT id FROM students WHERE id=?", values).fetchone():
        return True
    return False

@sqlite_decorate
def get_all_students_id(cur:sq.Cursor, values:list) -> list:
    return cur.execute("SELECT id FROM students").fetchall()

@sqlite_decorate
def get_group_students(cur:sq.Cursor, values:list) -> list:
    return cur.execute("SELECT id, name, user_name, state, score FROM students WHERE group_id=?", values).fetchall()

@sqlite_decorate
def change_student_state(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE students SET state=? WHERE id=?", values)

@sqlite_decorate
def get_student_state(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute("SELECT state FROM students WHERE id=?", values).fetchone()[0])

@sqlite_decorate
def get_student_score(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute("SELECT score FROM students WHERE id=?", values).fetchone()[0])

@sqlite_decorate
def change_score(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE students SET score=? WHERE id=?", values)

@sqlite_decorate
def get_message_students(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute("SELECT message FROM students WHERE id=?", values).fetchone()[0])

@sqlite_decorate
def change_message_students(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE students SET message=? WHERE id=?", values)

@sqlite_decorate
def get_students_group(cur:sq.Cursor, values:list) -> int:
    result = cur.execute("SELECT group_id FROM students WHERE id=?", values).fetchone()
    try:
        group_id = int(result[0])
    except:
        return None
    else:
        return group_id

@sqlite_decorate
def change_group_students(cur:sq.Cursor, values:list):
    cur.execute("UPDATE students SET group_id=? WHERE id=?", values)

@sqlite_decorate
def set_questions(cur:sq.Cursor, values:list) -> None:
    cur.execute("INSERT INTO questions(id, topic, file_id, question, variants) VALUES(?,?,?,?,?)", values)

@sqlite_decorate
def get_questions(cur:sq.Cursor, values:list) -> list:
    return cur.execute("SELECT id FROM questions WHERE topic=?", values).fetchall()

@sqlite_decorate
def get_question(cur:sq.Cursor, values:list) -> tuple:
    return cur.execute("SELECT file_id, question, variants FROM questions WHERE id=?", values).fetchone()

@sqlite_decorate
def check_question(cur:sq.Cursor, values:list) -> bool:
    if cur.execute("SELECT topic FROM questions WHERE topic=?", values).fetchone() is None:
        return False
    return True

@sqlite_decorate
def update_questions(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE questions SET variants=? WHERE id=?", values)

@sqlite_decorate
def get_new_id_questions(cur:sq.Cursor, values:list) -> int:
    result = cur.execute("SELECT id FROM questions", values).fetchall()
    if result != []:
        return int(result[-1][0]) + 1
    else:
        return 0 

@sqlite_decorate
def set_groups(cur:sq.Cursor, values:list) -> None:
    cur.execute("INSERT INTO groups(id, name, topic, message) VALUES(?, ?, ?, ?)", values)

@sqlite_decorate
def check_groups(cur:sq.Cursor, values:list) -> bool:
    if cur.execute("SELECT id FROM groups WHERE id=?", values).fetchone():
        return True
    return False

@sqlite_decorate
def update_groups(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE groups SET topic=? WHERE id=?", values)

@sqlite_decorate
def update_groups_message(cur:sq.Cursor, values:list) -> None:
    cur.execute("UPDATE groups SET message=? WHERE id=?", values)

@sqlite_decorate
def get_new_id_groups(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute("SELECT id FROM groups", values).fetchall()[-1][0])+1

@sqlite_decorate
def get_group_topic(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute('SELECT topic FROM groups WHERE id=?', values).fetchone()[0])

@sqlite_decorate
def get_id_from_name(cur:sq.Cursor, values:list) -> str:
    return cur.execute("SELECT id FROM groups WHERE name=?", values).fetchone()

@sqlite_decorate
def get_group_message(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute('SELECT message FROM groups WHERE id=?', values).fetchone()[0])

@sqlite_decorate
def set_marafon(cur:sq.Cursor, values:list) -> None:
    cur.execute("INSERT INTO marafon(id, file, question, answers) VALUES(?,?,?,?)", values)

@sqlite_decorate
def get_marafon(cur:sq.Cursor, values:list) -> tuple:
    return cur.execute("SELECT file, question, answers FROM marafon WHERE id=?", values).fetchone()

@sqlite_decorate
def get_new_id_marafon(cur:sq.Cursor, values:list) -> int:
    return int(cur.execute("SELECT id FROM marafon").fetchall()[-1][0])+1

@sqlite_decorate
def get_topic_name(cur:sq.Cursor, values:list) -> tuple:
    return cur.execute("SELECT name FROM topic WHERE id=?", values).fetchone()

@sqlite_decorate
def set_topic_name(cur:sq.Cursor, values:list) -> None:
    cur.execute("INSERT INTO topic(id, name) VALUES(?, ?)", values)
