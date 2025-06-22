from django.shortcuts import render
from Report.models import *
from django.db.models import Q 
from django.core.paginator import Paginator
from django.db.models import Sum
# Create your views here.
def get_students(request):
    querySet = Student.objects.all()  
    
    if request.GET.get('search'):
        search=request.GET.get('search')
        querySet=querySet.filter(
            Q(name__icontains=search) |
            Q(department__department__icontains=search) |
            Q(student_id__student_id__icontains=search) |
            Q(age__icontains=search) |
            Q(email__icontains=search) |
            Q(address__icontains=search)
        )
        
    
    paginator=Paginator(querySet,6)
    page_number=request.GET.get("page",1)
    page_obj=paginator.get_page(page_number)
    return render(request, './Pages/student.html', context={'Data': page_obj})

# Here Details of a user
from .seed import generate_report_card
def showResult(request,student_id):
    # Don't use this function use it once you have to seed the report card data
    # generate_report_card()
    querySet= SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = querySet.aggregate(total_marks=Sum('marks'))
    return render(request,"./Pages/student_Result.html",context={"Data":querySet,"total_marks":total_marks})