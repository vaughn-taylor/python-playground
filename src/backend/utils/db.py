
import sqlite3
import os
from contextlib import contextmanager

@contextmanager
def get_db_cursor():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'app.db'))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable row access by column name
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
