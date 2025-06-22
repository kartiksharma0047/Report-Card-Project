from django.contrib import admin

# Register your models here.
from .models import *
from django.db.models import Sum

admin.site.register(Student)
admin.site.register(StudentId)
admin.site.register(Subject)
admin.site.register(Department)

class SubjectMarkAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks'] 

admin.site.register(SubjectMarks, SubjectMarkAdmin)

class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'student_rank', 'total_marks', 'date_report_generation']
    ordering = ['student_rank']

    def total_marks(self, obj):
        subject_marks = SubjectMarks.objects.filter(student=obj.student)
        total = subject_marks.aggregate(marks=Sum('marks'))['marks']
        return total  # Don't use total['marks'] here

admin.site.register(ReportCard,ReportCardAdmin)