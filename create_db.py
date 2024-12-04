import sqlite3

def create_db():
    conn = sqlite3.connect('todo_list.db')
    # Tables creation scripts
    conn.execute("PRAGMA foreign_keys = ON") # Allowing foreign keys

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Users(
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
        );
        """)
    # One to one relationship
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS UserDetails(
        user_details_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        phone_number TEXT,
        preference TEXT,
        address TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
        );
        """)
    # One to many relationship
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Tasks(
        task_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        description TEXT,
        due_date DATE,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
        );""")
    # No relationship
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Tags(
        tag_id INTEGER PRIMARY KEY,
        name TEXT
        );""")
    # many to many relationship
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Tag_Task(
        task_id INTEGER,
        tag_id,
        PRIMARY KEY(task_id, tag_id),
        FOREIGN KEY(task_id) REFERENCES Tasks(task_id),
        FOREIGN KEY(tag_id) REFERENCES Tags(tag_id)
        );
        """)
    conn.commit() # saving the changes of the database
    conn.close() # closing the connection with the database

if __name__ == "__main__":
    create_db()
