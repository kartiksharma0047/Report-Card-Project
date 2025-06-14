from django.db import models

# Create your models here.

class Department(models.Model):
    department=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.department
    
    class Meta:
        ordering=['department']


class StudentId(models.Model):
    student_id=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.student_id 

class Subject(models.Model):
    subject_name=models.CharField(max_length=100)
    
    def __str__(self) ->str:
        return self.subject_name

class Student(models.Model):
    department=models.ForeignKey(Department, related_name="depart", on_delete=models.CASCADE)
    student_id=models.OneToOneField(StudentId, related_name="studentid", on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.IntegerField(default=18)
    email=models.EmailField(unique=True)
    address=models.TextField(null=True)
    
    def __str__(self)-> str:
        return self.name
    
    class Meta:
        ordering=['name']
        verbose_name='student'
        
        
class SubjectMarks(models.Model):
    student=models.ForeignKey(Student,related_name="studentmarks",on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks=models.IntegerField()
    
    # This will make one student and its subject appear in table only one time
    class Meta:
        unique_together=["student","subject"]
        
    def __str__(self)->str:
        return f"{self.student.name} {self.subject.subject_name}"