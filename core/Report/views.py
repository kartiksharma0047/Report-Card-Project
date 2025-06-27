from django.shortcuts import render
from Report.models import *
from django.core.paginator import Paginator
from django.db.models import Sum
# Create your views here.
from django.db.models import OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.shortcuts import redirect
from .utils import render_pdf_from_template, send_email_with_pdf


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
    querySet = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = querySet.aggregate(total_marks=Sum('marks')) or {'total_marks': 0}
    if not querySet.exists():
        return render(request, "./Pages/student_Result.html", context={"Data": [], "total_marks": 0, "percentile": 0})
    current_student = querySet.first().student

    all_students = Student.objects.all()
    marks_with_totals = []

    for student in all_students:
        total = SubjectMarks.objects.filter(student=student).aggregate(tm=Sum('marks'))['tm'] or 0
        marks_with_totals.append((student.id, total))

    # Sort students by total marks (descending)
    marks_with_totals.sort(key=lambda x: x[1], reverse=True)

    # Create a map of student_id -> rank
    rank_map = {student_id: idx + 1 for idx, (student_id, _) in enumerate(marks_with_totals)}

    # Get current student's rank
    rank = rank_map.get(current_student.id, len(all_students))

    # Calculate percentile on scale of 10
    percentile = round((rank / len(all_students)) * 10, 1)
    
    if request.GET.get('email_sent') == '1':
        messages.success(request, "Email sent successfully!")

    return render(
        request,
        "./Pages/student_Result.html",
        context={
            "Data": querySet,
            "total_marks": total_marks,
            "percentile": percentile
        }
    )
    
def email_report(request, student_id):
    # Get the student
    try:
        student = Student.objects.get(student_id__student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'Pages/error.html', {'message': 'Student not found.'})

    # Prepare data for PDF
    querySet = SubjectMarks.objects.filter(student=student)
    total_marks = querySet.aggregate(total_marks=Sum('marks')) or {'total_marks': 0}
    all_students = Student.objects.all()

    marks_with_totals = [(stu.id, SubjectMarks.objects.filter(student=stu).aggregate(tm=Sum('marks'))['tm'] or 0) for stu in all_students]
    marks_with_totals.sort(key=lambda x: x[1], reverse=True)
    rank_map = {sid: idx + 1 for idx, (sid, _) in enumerate(marks_with_totals)}
    rank = rank_map.get(student.id, len(all_students))
    percentile = round((rank / len(all_students)) * 10, 1)

    context = {
        "Data": querySet,
        "total_marks": total_marks,
        "percentile": percentile,
    }

    # Render PDF and send email
    filename = f"{student.name.replace(' ', '_')}_ReportCard.pdf"
    pdf_path = render_pdf_from_template('Pages/result_template.html', context, filename)
    if pdf_path:
        send_email_with_pdf(student, pdf_path)
        student.is_email_sent = True
        student.save()

    # Redirect to showResult with a flag
    return redirect(f'/result/{student.student_id.student_id}/?email_sent=1')