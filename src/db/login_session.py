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

    query = "SELECT username FROM cv_pt.public.sessions WHERE id = %s"
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

    query = "SELECT username FROM cv_pt.public.sessions WHERE id = %s"
    cursor.execute(query, (session_token,))
    result = cursor.fetchone()[0]

    db.close()
    return result if result is not None else None


def logout(mood_rating):
    try:
        with open(session_token_path, "r") as f:
            session_token = f.read().strip()
    except FileNotFoundError:
        return None

    from db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    # Calculate session duration
    query = "SELECT * FROM cv_pt.public.calculate_session_duration(%s)"
    cursor.execute(query, (session_token,))
    duration = cursor.fetchone()[0]

    # TODO: Add volume (by multiplying the number of reps by the weight used for each workout in the session)
    query = "SELECT * FROM cv_pt.public.end_session(%s, %s, %s, %s)"
    cursor.execute(query, (session_token, duration, 0, mood_rating))
    conn.commit()

    db.close()
    os.remove(session_token_path)
