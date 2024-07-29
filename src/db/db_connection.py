import psycopg2
from tkinter import messagebox


class DBConnection:

    conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname="cv_pt",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
            print("Connected to database")
            return self.conn
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def close(self):
        self.conn.cursor().close()
        self.conn.close()


if __name__ == "__main__":
    db = DBConnection()
    db.connect()
    db.close()
