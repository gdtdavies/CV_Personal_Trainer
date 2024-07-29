import os
import sys

session_token_path = os.path.join(os.path.dirname(__file__), './session_token.txt')
sys.path.append(os.path.join(os.path.dirname(__file__)))


def validate_session():
    try:
        with open(session_token_path, "r") as f:
            session_token = f.read().strip()
    except FileNotFoundError:
        return False

    from db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    query = "SELECT user_id FROM cv_pt.public.user_sessions WHERE session_token = %s"
    cursor.execute(query, (session_token,))
    result = cursor.fetchone()

    db.close()
    return result is not None


def get_user_id():
    try:
        with open(session_token_path, "r") as f:
            session_token = f.read().strip()
    except FileNotFoundError:
        return None

    from db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    query = "SELECT user_id FROM cv_pt.public.user_sessions WHERE session_token = %s"
    cursor.execute(query, (session_token,))
    result = cursor.fetchone()[0]

    db.close()
    return result if result is not None else None


def delete_session():
    try:
        with open(session_token_path, "r") as f:
            session_token = f.read().strip()
    except FileNotFoundError:
        print("Session token file not found")
        return

    from db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    print(session_token)
    query = 'SELECT * FROM cv_pt.public.delete_user_session(%s)'
    cursor.execute(query, (session_token,))
    conn.commit()

    db.close()

    os.remove(session_token_path)
