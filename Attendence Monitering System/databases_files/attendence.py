import sqlite3

# Connect to the database (this will create the database if it doesn't exist)
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
def insert_user(email, name):
    data = (email, name)
    cursor.execute("INSERT INTO Users (Email, Name) VALUES (?, ?);", data)
    conn.commit()


def display_users():
    # Retrieve and display data from the 'users' table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
def check_email_exists(email):
    cursor.execute("SELECT Email FROM Users WHERE Email = ?;", (email,))
    result = cursor.fetchone()
    if result:
        return 0  # Email found
    else:
        return 1  # Email not found

# Create the Users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        Email TEXT PRIMARY KEY,
        Name TEXT
    )
""")
#_________________________________________________________________________________________________________

def insert_subject(subject_name, user_email):
    data = (subject_name, user_email)
    cursor.execute("INSERT INTO Subjects (Subject_Name, User_Email) VALUES (?, ?);", data)
    conn.commit()

def display_subjects():
    cursor.execute("SELECT * FROM Subjects;")
    rows = cursor.fetchall()
    for row in rows:
        print("Subject Name:", row[0])
        print("User Email:", row[1])
        print()  # Add an empty line for separation



# Create the Subjects table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subjects (
        Subject_Name TEXT PRIMARY KEY,
        User_Email TEXT,
        FOREIGN KEY (User_Email) REFERENCES Users(Email)
    )
""")
#________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________



# Create the Lectures table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lectures (
        Lecture_ID INTEGER PRIMARY KEY,
        Subject_Name TEXT,
        Lecture_Number INTEGER,
        Date TEXT,
        FOREIGN KEY (Subject_Name) REFERENCES Subjects(Subject_Name)
    )
""")
#_______________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________

def display_students():
    cursor.execute("SELECT * FROM Students;")
    rows = cursor.fetchall()
    for row in rows:
        print("Roll No : ", row[0])
        print("Name : ", row[1])
        print() 


# Create the Students table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        Roll_Number TEXT PRIMARY KEY,
        Name TEXT
    )
""")

# Create the Attendance table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Attendance (
        Attendance_ID INTEGER PRIMARY KEY,
        Lecture_ID INTEGER,
        Roll_Number TEXT,
        Status TEXT,
        FOREIGN KEY (Lecture_ID) REFERENCES Lectures(Lecture_ID),
        FOREIGN KEY (Roll_Number) REFERENCES Students(Roll_Number)
    )
""")

