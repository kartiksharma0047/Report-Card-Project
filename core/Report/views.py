from django.shortcuts import render
from Report.models import *
from django.db.models import Q 
from django.core.paginator import Paginator
from django.db.models import Sum
# Create your views here.
from django.db.models import Q, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce

def get_students(request):
    querySet = Student.objects.all()
    search = request.GET.get('search')
    sort = request.GET.get('sort')
    if not sort:
        sort = 'name'  # Apply default sorting only if user didn't choose one


    # Apply search filter only on the selected sort field
    if search:
        if sort == 'student_id':
            querySet = querySet.filter(student_id__student_id__istartswith=search)
        elif sort == 'name':
            querySet = querySet.filter(name__istartswith=search)
        elif sort == 'email':
            querySet = querySet.filter(email__istartswith=search)
        elif sort == 'age':
            querySet = querySet.filter(age__istartswith=search)
        elif sort == 'address':
            querySet = querySet.filter(address__istartswith=search)
        elif sort == 'department':
            querySet = querySet.filter(department__department__istartswith=search)
        elif sort == 'rank':
            querySet = querySet.annotate(
                rank=Coalesce(
                    Subquery(
                        ReportCard.objects.filter(student=OuterRef('pk'))
                        .values('student_rank')[:1]
                    ),
                    9999,
                    output_field=IntegerField()
                )
            ).filter(rank__icontains=search)

    # Apply ordering (ascending only for now)
    if sort == 'student_id':
        querySet = querySet.order_by('student_id__student_id')
    elif sort == 'name':
        querySet = querySet.order_by('name')
    elif sort == 'email':
        querySet = querySet.order_by('email')
    elif sort == 'age':
        querySet = querySet.order_by('age')
    elif sort == 'address':
        querySet = querySet.order_by('address')
    elif sort == 'department':
        querySet = querySet.order_by('department__department')
    elif sort == 'rank':
        querySet = querySet.annotate(
            rank=Coalesce(
                Subquery(
                    ReportCard.objects.filter(student=OuterRef('pk'))
                    .values('student_rank')[:1]
                ),
                9999,
                output_field=IntegerField()
            )
        ).order_by('rank')

    paginator = Paginator(querySet, 6)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, './Pages/student.html', context={'Data': page_obj})

# Here Details of a user
from .seed import generate_report_card
def showResult(request,student_id):
    # Don't use this function use it once you have to seed the report card data
    # generate_report_card()
    querySet= SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = querySet.aggregate(total_marks=Sum('marks'))
    return render(request,"./Pages/student_Result.html",context={"Data":querySet,"total_marks":total_marks})