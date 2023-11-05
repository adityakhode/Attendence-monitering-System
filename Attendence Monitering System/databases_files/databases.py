import sqlite3


def display():
    # Retrieve and display data from the 'users' table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
def insert_user_table( name ,phone ,email ,password,gfm_role):
    data = (name ,phone ,email ,password,gfm_role)
    cursor.execute("INSERT INTO users (name, phone_no, email_id, password,gfm_role) VALUES (?, ?, ?, ?, ?);", data)
    conn.commit()

def check_name_exists(value):
    # Try to find the value in the user table
    cursor.execute("SELECT * FROM users WHERE name = ? OR phone_no = ? OR email_id = ? ",(value, value, value))
    result = cursor.fetchone()  # Fetch the first matching row
    if result:
        return 1  # Value found exactly
    else:
        return 0  # Value not found
    
def check_password_exists(value):
    # Try to find the value in the user table
    cursor.execute("SELECT * FROM users WHERE password = ?",(value,))
    result = cursor.fetchone()  # Fetch the first matching row
    if result:
        return 1  # Value found exactly
    else:
        return 0  # Value not found

def get_email_id_by_value(value):
    # Try to find the value in the user table
    cursor.execute("SELECT email_id FROM users WHERE name = ? OR phone_no = ? OR email_id = ?", (value, value, value))
    result = cursor.fetchone()  # Fetch the first matching row
    return result[0]  # Return the name of the user found

def get_name_by_value(value):
    # Try to find the value in the user table
    cursor.execute("SELECT name FROM users WHERE name = ? OR phone_no = ? OR email_id = ?", (value, value, value))
    result = cursor.fetchone()  # Fetch the first matching row
    return result[0]  # Return the name of the user found

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('login_credentials.db')
cursor = conn.cursor()

# Check if the 'users' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
if not cursor.fetchone():
    # Create the 'users' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE users (
            sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_no INTEGER NOT NULL,
            email_id TEXT NOT NULL,
            password TEXT NOT NULL,
            gfm_role TEXT NOT NULL
        );
    ''')
    conn.commit()
