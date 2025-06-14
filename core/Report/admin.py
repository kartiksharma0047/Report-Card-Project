from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Student)
admin.site.register(StudentId)
admin.site.register(Subject)
admin.site.register(Department)

class SubjectMarkAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks'] 

admin.site.register(SubjectMarks, SubjectMarkAdmin)