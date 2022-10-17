import sqlite3 as sl
import sys
import time
import os

# Tamam.
def letter_grade_to_score(letter):
    if letter == 'AA':
        return 4
    elif letter == 'BA':
        return 3.5
    elif letter == 'BB':
        return 3
    elif letter == 'CB':
        return 2.5
    elif letter == 'CC':
        return 2
    elif letter == 'DC':
        return 1.5
    elif letter == 'DD':
        return 1
    elif letter == 'FF' or letter == 'VF':
        return 0

# Tamam.
def user_type_choices(user_type):
    if user_type == '1':
        user_one()
    elif user_type == '2':
        user_two()
    elif user_type == '3':
        user_three()

# Tamam.
def user_three():
    os.remove('grades.db')
    print('Database cleaned.')
    time.sleep(0.5)
    ask_user_type()

# Tamam.
def get_course_info():
    print("""Enter your lecture name/code and letter graders\n(AA-BA-BB-CB-CC-DC-DD-FF-VF) respectively.""")
    cont = None
    list_of_grades = []
    while cont != 'q':
        time.sleep(0.2)
        course_name = input('Enter the course name: ')
        while True:
            credit = input("Enter the credit of this course:")
            if credit in ['1','1.5','2','2.5','3','3.5','4','4.5','5']:
                credit = float(credit)
                break
            else:
                print("Enter correct amount of credits !\n1 - 1.5 - 2 - 2.5 - 3 - 3.5 - 4 - 4.5 - 5 : ")
                
        while True:
            letter_grade = input("""Enter the letter grade\n(AA-BA-BB-CB-CC-DC-DD-FF-VF) : """)
            if letter_grade in ['AA','BA','BB','CB','CC','DC','DD','FF','VF']:
                break
            else:
                print("Enter the grade in correct form.")
                
        list_of_grades.append((course_name,credit,letter_grade))
        print("GRADES TO BE ADDED\n")
        for lecture in list_of_grades:
            print("""
                  Lecture: {}  Credit: {}  Grade: {}
                  """.format(lecture[0],lecture[1], lecture[2]))
        print("\n\n")          
        time.sleep(0.3)
        cont = input("To continue press Enter.\nTo quit enter 'q': ")
        
    print("\n\nThe grades are added into the system.")
    return list_of_grades

# Tamam.
def user_one():
    con = sl.connect('grades.db')
    
    with con:
        con.execute("""
            CREATE TABLE GRADES (
                course_name TEXT NOT NULL PRIMARY KEY,
                credit FLOAT NOT NULL,
                letter_grade TEXT
            );
        """)
    list_of_grades = get_course_info()
        
    sql = 'INSERT INTO GRADES (course_name,credit,letter_grade) values(?,?,?)'
    with con:
        con.executemany(sql,list_of_grades)
    con.close()
    print("\n\nDirecting you to the main menu...\n\n")
    time.sleep(2)
    ask_user_type()

# Tamam.
def user_two():
    choice = ask_choice_to_user_two()
    
    if choice == 1:
        show_courses_gpa()
    elif choice == 2:
        show_gpa()
    elif choice == 3:
        add_course()
    elif choice == 4:
        update_course()
    elif choice == 5:
        delete_course()
        
    user_two()
    
# Tamam.
def calculate_gpa(credits,grades,number_of_recs):
    total_point = 0
    for i in range(number_of_recs):
        total_point += letter_grade_to_score(grades[i]) * credits[i]
    return round(total_point / sum(credits),2)
   
# Tamam.     
def add_course():
    con = sl.connect('grades.db')
    list_of_grades = get_course_info()
        
    sql = 'INSERT INTO GRADES (course_name,credit,letter_grade) values(?,?,?)'
    with con:
        con.executemany(sql,list_of_grades)
    con.close()

# Tamam.
def update_course():
    while True:
        courses = show_courses_gpa()
        code = input("Enter course code to be updated: ")
        if code in courses:
            break
        else:
            print("There is no such course !")
            time.sleep(0.5)

    while True:
        credit = input("Enter the credit of this course:")
        if credit in ['1','1.5','2','2.5','3','3.5','4','4.5','5']:
            credit = float(credit)
            break
        else:
            print("Enter correct amount of credits !\n1 - 1.5 - 2 - 2.5 - 3 - 3.5 - 4 - 4.5 - 5 : ")
                
    while True:
        letter_grade = input("""Enter the letter grade\n(AA-BA-BB-CB-CC-DC-DD-FF-VF) : """)
        if letter_grade in ['AA','BA','BB','CB','CC','DC','DD','FF','VF']:
            break
        else:
            print("Enter the grade in correct form.")
    conn = sl.connect('grades.db')
    sql = ''' UPDATE GRADES
              SET credit = ? ,
                  letter_grade= ?
              WHERE course_name = ?'''
    cur = conn.cursor()
    cur.execute(sql, [credit,letter_grade, code])
    conn.commit()
    print("The course '" + code + "' is updated on database.")
    conn.close()

# Tamam.    
def delete_course():
    conn = sl.connect('grades.db')
    while True:
        courses = show_courses_gpa()
        code = input("Enter course code to be deleted: ")
        if code in courses:
            break
        else:
            print("There is no such course !")
            time.sleep(0.5)
    sql = 'DELETE FROM GRADES WHERE course_name=?'
    cur = conn.cursor()
    cur.execute(sql, (code,))
    conn.commit()
    print("The course '" + code + "' is deleted from database.")
    conn.close()
  
# Tamam.
def show_courses_gpa():
    grades =[]
    credits = []
    courses = []
    con = sl.connect('grades.db')
    with con:
        data = con.execute("SELECT * FROM GRADES")
    print("Lecture       Credit       Grade")
    for row in data:
        print(row[0]+"          "+str(row[1])+"           "+row[2])
        credits.append(row[1])
        grades.append(row[2])
        courses.append(row[0])
    gpa  = calculate_gpa(credits, grades, len(grades))
    print("\nOverall GPA: " + str(gpa))
    con.close()
    return courses

# Tamam.
def show_gpa():
    grades =[]
    credits = []
    con = sl.connect('grades.db')
    with con:
        data = con.execute("SELECT * FROM GRADES")
    for row in data:
        credits.append(row[1])
        grades.append(row[2])
    gpa  = calculate_gpa(credits, grades, len(grades))
    print("\nOverall GPA: " + str(gpa))
    con.close()

# Tamam.
def ask_choice_to_user_two():
    choice = None
    time.sleep(0.5)
    while not (choice in ['1','2','3','4','5','q']):
        print("****************************************************************************")
        choice = input("""
                       Menu
                       
                       1- Show all courses and overall GPA.
                       2- Show overall GPA.
                       3- Add new course.
                       4- Update a course.
                       5- Delete a course.
                       
                       'q' - Exit the program.
                       Enter: """)
                      
        if choice == 'q':
            print("Have a nice day !")
            sys.exit()
    return int(choice)

# Tamam.
def ask_user_type():
    user_type = None
        
    while user_type != '1' and user_type != '2' and user_type != '3' and user_type != 'q':
        print("****************************************************************************")
        user_type = input(
              """
              Welcome to Genius GPA Calculator !
              
              Please select one of the options below:
                  
                  1- Create the database for grade records.
                  
                  2- I already have records in database.
                  
                  3- Clean all previous records.
                  
                 'q'- Exit the program.
              
                Enter '1', '2', '3' or 'q' : """
              )
    if user_type == 'q':
        print('Have a nice day !')
        sys.exit()
    else:
        user_type_choices(user_type)

try:
    ask_user_type()
    
except sl.OperationalError:
    print("There is no previous record.")
    
finally:
    print("Have a nice day !")