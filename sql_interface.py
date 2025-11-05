import mysql.connector
import os
import pickle
import pandas

DATABASE_NAME = "USEMP_DB"
STUDENT_TABLE_NAME = "STUDENT_USEMP_TBL"
EXAM_TABLE_NAME = "EXAMINATION_USEMP_TBL"
FILENAME = "login-cred.usemp"

# con = None
# cur = None

class login:
    def __init__(self, uname, password):
        self.uname = uname
        self.password = password

def get_login(): 
    login_cred = None
    if FILENAME in os.listdir('.'):
        with open(FILENAME, 'rb') as fb:
            login_cred = pickle.load(fb)
            # print(login_cred.uname, login_cred.password)
    else:
        print("Login credentials not found. Please enter your login credentials")
        user = input("Enter the username: ")
        pw = input("Enter the password: ")
        login_cred = login(user, pw)
        with open(FILENAME, 'wb') as fb:
            pickle.dump(login_cred, fb)

    return login_cred


def SQL_INIT():
    global con
    global cur
    # if os.name == "posix":
    #     os.system("mysql.server start")
    #     os.wait(3)

    login_cred = get_login()

    con = mysql.connector.connect(user=login_cred.uname, password=login_cred.password)

    if not con.is_connected():
        print("Please ensure a MySQL Server is running to start using this program.")
        return

    cur = con.cursor()

    cur.execute("SHOW DATABASES")
    databases = [x[0] for x in cur.fetchall()]

    if DATABASE_NAME not in databases:
        cur.execute(f"CREATE DATABASE {DATABASE_NAME}")
        cur.execute(f"USE {DATABASE_NAME}")
        cur.execute(f"CREATE TABLE `{STUDENT_TABLE_NAME}` (Student_ID INT PRIMARY KEY, Name VARCHAR(30) NOT NULL, SLOT ENUM('MORNING', 'EVENING') NOT NULL)")
        cur.execute(f"CREATE TABLE `{EXAM_TABLE_NAME}` (EXAM_ID INT PRIMARY KEY, Student_ID INT, FOREIGN KEY (Student_ID) REFERENCES `{STUDENT_TABLE_NAME}`(Student_ID), PHYSICS INT, CHEMISTRY INT, MATH INT, PYTHON INT, EXAM ENUM('CAT1', 'CAT2', 'FAT'))")
    else:
        cur.execute(f"USE {DATABASE_NAME}")
    
    #os.system("mysql.server stop")

def write_to_csv(): 
    global con
    global cur

    
    cur.execute(f"SELECT * FROM {STUDENT_TABLE_NAME}")
    students = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    df = panda.DataFrame(students, columns=columns)

    df.to_csv("students.csv", index=False)


    cur.execute(f"SELECT * FROM {EXAM_TABLE_NAME}")
    exams = cur.fetchall()


SQL_INIT()

