import mysql.connector
import os
import pickle

DATABASE_NAME = "USEMP_DB"
STUDENT_TABLE_NAME = "STUDENT_USEMP_TBL"
EXAM_TABLE_NAME = "EXAMINATION_USEMP_TBL"
FILENAME = "login-cred.usemp"

class login:
    def __init__(self, uname, password):
        self.uname = uname
        self.password = password

def SQL_INIT():
    # if os.name == "posix":
    #     os.system("mysql.server start")
    #     os.wait(3)

    if FILENAME in os.listdir('.'):
        with open(FILENAME, 'rb') as fb:
            login_cred = pickle.load(fb)
            print(login_cred.uname, login_cred.password)
    else:
        print("Login credentials not found. Please enter your login credentials")
        user = input("Enter the username: ")
        pw = input("Enter the password: ")
        login_cred = login(user, pw)
        with open(FILENAME, 'wb') as fb:
            pickle.dump(login_cred, fb)


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
    
    #os.system("mysql.server stop")

SQL_INIT()