import csv
import random

def read_students(file_path):
    students = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append(row['S#'])
    return students

def read_courses(file_path):
    courses = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            courses.append(row['C#'])
            #print(row)
    return courses

def generate_grade():
    if random.random() < 0.2:
        return round(random.uniform(40, 59), 1)
    else:
        return round(random.uniform(60, 100), 1)

def generate_student_courses(students, courses, n):
    student_courses = []
    for i in range(n):
        student_id = students[i]
        num_courses = random.randint(30, 50)
        selected_courses = random.sample(courses, num_courses)
        for course_id in selected_courses:
            grade = generate_grade()
            student_course = {
                'S#': student_id,
                'C#': course_id,
                'GRADE': grade
            }
            student_courses.append(student_course)
            print(student_course)
    print(i)
    return student_courses

def write_student_courses(file_path, student_courses):
    with open(file_path, 'w',newline='') as csvfile:
        fieldnames = ['S#', 'C#', 'GRADE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(student_courses)

if __name__ == '__main__':
    students = read_students('C:/Users/Jiefucious/Desktop/Student1.csv')
    courses = read_courses('C:/Users/Jiefucious/Desktop/c034.csv')
    student_courses = generate_student_courses(students, courses, 5000)  # n = amount of students
    write_student_courses('C:/Users/Jiefucious/Desktop/sc.csv', student_courses)
