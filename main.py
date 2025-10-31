import mysql.connector

DATABASE_NAME = "USEMP_DB"
STUDENT_TABLE_NAME = "STUDENT_USEMP_TBL"
EXAM_TABLE_NAME = "EXAMINATION_USEMP_TBL"

con = mysql.connector.connect(user="root", password="")
cur = con.cursor()

cur.execute("SHOW DATABASES")
databases = [x[0] for x in cur.fetchall()]

if DATABASE_NAME not in databases:
    cur.execute(f"CREATE DATABASE {DATABASE_NAME}")
    cur.execute(f"USE {DATABASE_NAME}")
    cur.execute(f"CREATE TABLE `{STUDENT_TABLE_NAME}` (Student_ID INT PRIMARY KEY, Name VARCHAR(30) NOT NULL, SLOT ENUM('MORNING', 'EVENING') NOT NULL)")
    cur.execute(f"CREATE TABLE `{EXAM_TABLE_NAME}` (EXAM_ID INT PRIMARY KEY, Student_ID INT, FOREIGN KEY (Student_ID) REFERENCES `{STUDENT_TABLE_NAME}`(Student_ID), PHYSICS INT, CHEMISTRY INT, MATH INT, PYTHON INT, EXAM ENUM('CAT1', 'CAT2', 'FAT'))")