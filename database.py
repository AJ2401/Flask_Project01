import sqlite3


def create_user(username, email, password, contact_number, otp):
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password, contact_number, otp) VALUES (?, ?, ?, ?, ?)",
              (username, email, password, contact_number, otp))
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()

    if user is None:
        return None
    else:
        return {
            'username': user[1],
            'email': user[2],
            'password': user[3],
            'contact_number': user[4],
            'otp': user[5]
        }


def get_user_by_username(username):
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user is None:
        return None
    else:
        return {
            'username': user[1],
            'email': user[2],
            'password': user[3],
            'contact_number': user[4],
            'otp': user[5]
        }


def update_user(username, field, value):
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute(
        f"UPDATE users SET {field} = ? WHERE username = ?", (value, username))
    conn.commit()
    conn.close()
