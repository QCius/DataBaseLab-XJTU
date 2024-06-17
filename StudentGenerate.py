import csv
import random
import datetime
from faker import Faker

def generate_name():
    fake = Faker("zh_CN")
    return fake.name()

def generate_birthdate():
    start_date = datetime.date(2002, 1, 1)
    end_date = datetime.date(2005, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + datetime.timedelta(days=random_days)

def generate_dorm():
    dorm_area = random.choice(["东", "西"])
    dorm_number = random.randint(101, 999)
    return f"{dorm_area}舍 {dorm_number}"

def generate_students(n):
    student_ids = set()
    with open('C:/Users/Jiefucious/Desktop/student1.csv', 'w',newline='') as csvfile:
        fieldnames = ['S#', 'SNAME', 'SEX', 'BDATE', 'HEIGHT', 'DORM']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(n):
            while True:
                student_id = f"{random.randint(10000000, 99999999)}"
                if student_id not in student_ids:
                    student_ids.add(student_id)
                    break

            student_name = generate_name()
            student_sex = random.choice(["男", "女"])
            student_birthdate = generate_birthdate()
            student_height = round(random.uniform(1.6, 1.95), 2)
            student_dorm = generate_dorm()

            student_data = {
                'S#': student_id,
                'SNAME': student_name,
                'SEX': student_sex,
                'BDATE': student_birthdate.strftime("%Y-%m-%d"),
                'HEIGHT': student_height,
                'DORM': student_dorm
            }
            print(i)
            print(student_data)
            writer.writerow(student_data)

if __name__ == '__main__':
    generate_students(5000)
