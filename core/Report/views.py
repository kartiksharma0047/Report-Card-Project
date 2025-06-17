from django.shortcuts import render
from Report.models import *
from django.db.models import Q 
from django.core.paginator import Paginator
# Create your views here.
def get_students(request):
    querySet = Student.objects.all()  
    
    if request.GET.get('search'):
        search=request.GET.get('search')
        querySet=querySet.filter(name__icontains=search)
    
    paginator=Paginator(querySet,6)
    page_number=request.GET.get("page",1)
    page_obj=paginator.get_page(page_number)
    return render(request, './Pages/student.html', context={'Data': page_obj})