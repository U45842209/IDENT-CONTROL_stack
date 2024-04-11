import mysql.connector


class Mysql:

    def __init__(self):
        self.mydb, self.sql_cursor = self.connect()

    @staticmethod
    def connect():
        try:
            mydb = mysql.connector.connect(
                host="172.20.0.10",
                user="root",
                password="password",
                database="bottle"
            )
            return mydb, mydb.cursor()
        except Exception as e:
            return e

    def find_user(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            val = (username,)
            self.sql_cursor.execute(sql, val)
            myresult = self.sql_cursor.fetchall()
            return myresult
        except Exception as e:
            return e

    def find_email(self, email):
        try:
            sql = "SELECT * FROM users WHERE email = %s"
            val = (email,)
            self.sql_cursor.execute(sql, val)
            myresult = self.sql_cursor.fetchall()
            return myresult
        except Exception as e:
            return e

    def register_user(self, username, hashed_password, email):
        try:
            sql = "INSERT INTO users (username, password_hash, email) VALUES (%s,%s,%s)"
            val = (username, hashed_password, email)
            self.sql_cursor.execute(sql, val)
            self.mydb.commit()
            return "success"
        except Exception as e:
            return "error"

    def get_user_info(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            val = (username,)
            self.sql_cursor.execute(sql, val)
            myresult = self.sql_cursor.fetchall()
            return myresult
        except Exception as e:
            return e

