import sqlite3
import os

# Connect to the database
db_name = "mydb.db"
db_path = os.path.join(os.getcwd(), db_name)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create the student table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT,
        password TEXT,
        photo TEXT
    )
""")

# Create the task table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        task_date DATE
    )
""")

# Create the history table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        task_date DATE
    )
""")

# Insert sample data into the student table
cur.execute("INSERT INTO student (fullname, email, password, photo) VALUES (?, ?, ?, ?)", ("John Doe", "john@example.com", "password123", "john_photo.jpg"))
cur.execute("INSERT INTO student (fullname, email, password, photo) VALUES (?, ?, ?, ?)", ("Alice Smith", "alice@example.com", "alice_password", "alice_photo.jpg"))

# Insert sample data into the task table
cur.execute("INSERT INTO task (task_name, task_date) VALUES (?, ?)", ("Complete assignment", "2024-04-07"))
cur.execute("INSERT INTO task (task_name, task_date) VALUES (?, ?)", ("Attend meeting", "2024-04-08"))

# Insert sample data into the history table
cur.execute("INSERT INTO history (task_name, task_date) VALUES (?, ?)", ("Review project proposal", "2024-04-05"))
cur.execute("INSERT INTO history (task_name, task_date) VALUES (?, ?)", ("Submit monthly report", "2024-03-30"))

# Commit changes and close the database connection
conn.commit()
conn.close()
