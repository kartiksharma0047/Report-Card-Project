import random
from faker import Faker
from .models import *
from django.db.models import Sum

fake=Faker()

def create_subject_marks(n):
    try:
        student_obj=Student.objects.all()
        for student in student_obj:
            subjects=Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0,100)
                )
    except Exception as e:
        print(e)

def seed_db(n)->None:
    try:
        for _ in range(n):
            departments_objs=Department.objects.all()
            random_index=random.randint(0,len(departments_objs)-1)
            student_id=f"STU-0{random.randint(100,999)}"
            department=departments_objs[random_index]
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(20,30)
            student_address=fake.address()
            
            student_id_obj=StudentId.objects.create(student_id=student_id)
            
            student_ob=Student.objects.create(
                department=department,
                student_id=student_id_obj,
                age=student_age,
                name=student_name,
                email=student_email,
                address=student_address
            )
    except Exception as e:
        print(e)
        
def generate_report_card():
    currentRank=-1
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-age')
    i=1
    for rank in ranks:
        ReportCard.objects.create(
            student=rank,
            student_rank=i
        )
        i=i+1