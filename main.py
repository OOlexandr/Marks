import sqlite3
from faker import Faker
from random import randint
from multiprocessing import Process, Event, Manager
from datetime import date

fake = Faker()
n_groups = 3
n_students = randint(30, 50)
n_subjects = 5
subjects = ["linear algebra", "calculus", "statistics", "language", "physics"]
n_teachers = randint(3, 5)
n_marks = 20

database = "marks.db"

def random_date():
    #generates a date between start of current year and today
    today = date.today()
    return date(today.year, randint(1, today.month), randint(1, today.day))

def writing_in_database(students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data):
    with sqlite3.connect(database) as db:
        cur = db.cursor()
        
        cur.execute("""DROP TABLE IF EXISTS groups""")
        cur.execute("""DROP TABLE IF EXISTS students""")
        cur.execute("""DROP TABLE IF EXISTS teachers""")
        cur.execute("""DROP TABLE IF EXISTS subjects""")
        cur.execute("""DROP TABLE IF EXISTS marks""")

        cur.execute("""CREATE TABLE groups(
	        id INTEGER PRIMARY KEY AUTOINCREMENT);""")

        cur.execute("""CREATE TABLE students(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        group_id INT,
	        name CHAR(30),
	        FOREIGN KEY (group_id) REFERENCES groups (id)
		        ON DELETE SET NULL
		        ON UPDATE CASCADE);""")

        cur.execute("""CREATE TABLE teachers(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        name CHAR(30));""")

        cur.execute("""CREATE TABLE subjects(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        name CHAR(30),
	        teacher_id INT,
	        FOREIGN KEY (teacher_id) REFERENCES teachers (id)
		        ON DELETE SET NULL
		        ON UPDATE CASCADE);""")

        cur.execute("""CREATE TABLE marks(
	        subject_id INT,
	        student_id INT,
	        mark INT,
	        mark_date DATE,
	        FOREIGN KEY (subject_id) REFERENCES subjects (id)
		        ON DELETE SET NULL
		        ON UPDATE CASCADE,
	        FOREIGN KEY (student_id) REFERENCES students (id)
		        ON DELETE SET NULL
		        ON UPDATE CASCADE);""")
        

        for i in range(n_groups):
            cur.execute("""INSERT INTO groups DEFAULT VALUES;""")
        
        students_prepared.wait()
        cur.executemany("""INSERT INTO students (group_id, name) VALUES (?, ?);""", data["students"])

        teachers_prepared.wait()
        cur.executemany("""INSERT INTO teachers (name) VALUES (?)""", data["teachers"])

        subjects_prepared.wait()
        cur.executemany("""INSERT INTO subjects (name, teacher_id) VALUES (?, ?)""", data["subjects"])

        marks_prepared.wait()
        cur.executemany("""INSERT INTO marks (subject_id, student_id, mark, mark_date) VALUES (?, ?, ?, ?)""", data["marks"])
        

def preparing_data(students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data):
    for i in range(n_students):
        data["students"].append((randint(1, n_groups), fake.name()))
    students_prepared.set()

    for i in range(n_teachers):
        data["teachers"].append((fake.name(),))
    teachers_prepared.set()
    
    for i in range(n_subjects):
        data["subjects"].append((subjects[i], randint(1, n_teachers)))
    subjects_prepared.set()
    
    today = date.today()
    for s in range(1, n_students+1):
        for i in range(n_marks):
            data["marks"].append((randint(1, n_subjects), s, randint(1, 100), random_date()))
    marks_prepared.set()
        

def main():
    students_prepared = Event()
    teachers_prepared = Event()
    subjects_prepared = Event()
    marks_prepared = Event()

    man = Manager()
    data = man.dict()
    data["students"] = man.list()
    data["teachers"] = man.list()
    data["subjects"] = man.list()
    data["marks"] = man.list()

    writing = Process(target=writing_in_database,
                        args=(students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data))
    preparing = Process(target=preparing_data,
                        args=(students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data))
    
    writing.start()
    preparing.start()

    preparing.join()
    writing.join()


if __name__ == '__main__':
    main()


    
#for i in range(n_teachers):
#    teacher = (fake.name(),)
#    cur.execute("""INSERT INTO teachers (name) VALUES (?);""", teacher)