import sqlite3

def get_connection():
    """
    Function to database sql
    """
    return sqlite3.connect('todo_list.db')


# =================Users Table===================


def check_user_existence(conn, user_id):
    cursor = conn.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        return False
    return True
    

def read_users():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return users


def read_user(user_id):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    cursor = conn.execute("SELECT * FROM Users WHERE user_id = ?", (user_id, ))
    user = cursor.fetchone()
    conn.close()
    return user


def add_user(name, email):
    conn = get_connection()
    conn.execute("INSERT INTO Users(name, email) VALUES(?, ?)", (name, email))
    print("User added successfully.")
    conn.commit()
    conn.close()


def update_user(user_id, name, email):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    conn.execute("UPDATE Users SET name = ?, email = ? WHERE user_id = ?", (name, email, user_id))
    conn.commit()
    conn.close()
    return 1


def delete_user(user_id):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    conn.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM UserDetails WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True


# =================Tasks Table====================


def check_task_existence(conn, task_id):
    cursor = conn.execute("SELECT 1 FROM Tasks WHERE task_id = ?", (task_id,))
    if cursor.fetchone() is None:
        return False
    return True


def read_tasks_for_user(user_id):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    cursor = conn.execute("SELECT * FROM Tasks WHERE user_id = ?", (user_id, ))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def add_task(user_id, description,due_date, status):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    conn.execute("INSERT INTO Tasks(user_id, description, due_date, status) VALUES(?, ?, ?, ?)", (user_id, description, due_date, status))
    print("Task added successfully.")
    conn.commit()
    conn.close()
    return True


def update_task( task_id, description, due_date, status):
    conn = get_connection()
    if not check_task_existence(conn, task_id):
        conn.close()
        print("Invalid Task ID.")
        return False
    conn.execute("UPDATE Tasks SET description = ?, due_date = ?, status = ? WHERE task_id = ?", (description ,due_date, status, task_id))
    conn.commit()
    conn.close()
    return True


def check_task(task_id):
    conn = get_connection()
    if not check_task_existence(conn, task_id):
        conn.close()
        print("Invalid Task ID.")
        return False
    conn.execute("UPDATE Tasks SET status = 'COMPLETE' WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True

    
def delete_task(task_id):
    conn = get_connection()
    conn = get_connection()
    if not check_task_existence(conn, task_id):
        conn.close()
        return False
    conn.execute("DELETE FROM Tasks WHERE task_id = ?", (task_id,))
    conn.execute("DELETE FROM Tag_Task WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()


# ======================User Details Table=========================


def read_user_details(user_id):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    cursor = conn.execute("SELECT * FROM UserDetails WHERE user_id = ?", (user_id,))
    user_details = cursor.fetchone()
    conn.close()
    return user_details


def add_user_details(user_id, phone, address, preference):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("There is no such user. Enter a valid User ID to add details.")
        return False
    
    cursor = conn.execute("SELECT 1 from UserDetails WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is not None:
        print("This user already has a user details record. If you want to update it please choose the update option.")
        return False

    conn.execute("INSERT INTO UserDetails(user_id, phone_number, address, preference) VALUES(?, ?, ?, ?)", (user_id, phone, address, preference))
    print("UserDetails added successfully.")
    conn.commit()
    conn.close()
    return True


def update_user_details(user_id, phone, address, preference):
    conn = get_connection()
    if not check_user_existence(conn, user_id):
        conn.close()
        print("Invalid User ID.")
        return False
    conn = get_connection()
    conn.execute("UPDATE UserDetails SET phone_number = ?, address = ?, preference = ? WHERE user_id = ?", (phone, address, preference, user_id))
    conn.commit()
    conn.close()
    return True


# ========================Tags Table==========================


def check_tag_existence(conn, tag_id):
    cursor = conn.execute("SELECT 1 FROM Tags WHERE tag_id = ?", (tag_id,))
    if cursor.fetchone() is None:
        return False
    return True


def read_tags():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM Tags")
    tags = cursor.fetchall()
    conn.close()
    return tags


def add_tag(name):
    conn = get_connection()
    conn.execute("INSERT INTO Tags(name) VALUES(?)", (name,))
    print("Tag added successfully.")
    conn.commit()
    conn.close()


def update_tag(tag_id ,name):
    conn = get_connection()
    if not check_tag_existence(conn, tag_id):
        conn.close()
        print("Invalid Tag ID.")
        return False
    conn.execute("UPDATE Tags SET name = ? WHERE tag_id = ?", (name, tag_id))
    conn.commit()
    conn.close()
    return True


def delete_tag(tag_id):
    conn = get_connection()
    if not check_tag_existence(conn, tag_id):
        conn.close()
        print("Invalid Tag ID.")
        return False
    conn.execute("DELETE FROM Tags WHERE tag_id = ?", (tag_id,))
    conn.commit()
    conn.close()
    return True


# =====================Tasks-Tags Table==========================


def read_tasks_for_tags(tag_id):
    conn = get_connection()
    if check_tag_existence(conn, tag_id) == False:
        conn.close()
        print("Invalid Tag ID.")
        return False
    cursor = conn.execute("SELECT task_id FROM Tag_Task WHERE tag_id = ?", (tag_id, ))
    tasks = cursor.fetchall()
    conn.close()
    return tasks # [tasks[0] for task in tasks]


def read_tags_for_task(task_id):
    conn = get_connection()
    if not check_task_existence(conn, task_id):
        conn.close()
        print("Invalid Task ID.")
        return False
    cursor = conn.execute("SELECT tag_id FROM Tag_Task WHERE task_id = ?", (task_id, ))
    tags = cursor.fetchall()
    conn.close()
    return tags  # [tags[0] for tag in tags]


def add_task_tag(task_id, tag_id):
    conn = get_connection()
    if check_task_existence(conn, task_id) == False or check_tag_existence(conn, tag_id) == False:
        conn.close()
        print("Invalid Tag ID or Task ID.")
        return False
    conn.execute("INSERT INTO Tag_Task(task_id, tag_id) VALUES(?, ?)", (task_id, tag_id))
    conn.commit()
    conn.close()
    return True


def delete_task_tag(task_id, tag_id):
    conn = get_connection()
    if check_task_existence(conn, task_id) == False or check_tag_existence(conn, tag_id) == False:
        conn.close()
        print("Invalid Tag ID or Task ID.")
        return False
    conn.execute("DELETE FROM Tag_Task WHERE task_id = ? AND tag_id = ?", (task_id, tag_id))
    conn.commit()
    conn.close()
    return True