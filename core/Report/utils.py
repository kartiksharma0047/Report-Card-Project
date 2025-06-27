from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import os
from django.conf import settings
from .models import ReportCard
from django.core.mail import EmailMessage

def render_pdf_from_template(template_src, context, filename):
    html = render_to_string(template_src, context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        pdf_dir = os.path.join(settings.BASE_DIR, 'Student_Result_pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        path = os.path.join(pdf_dir, filename)
        
        with open(path, 'wb') as output:
            output.write(result.getvalue())
        return path
    return None


def send_email_with_pdf(student, pdf_path):
    context = {'student': student}
    message = render_to_string('Pages/email_template.html', context)

    email = EmailMessage(
        subject="Your Report Card",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[student.email],
    )
    email.content_subtype = "html"
    email.attach_file(pdf_path)

    try:
        email.send()
        
        # ✅ Update is_email_sent = True for latest ReportCard
        latest_report = ReportCard.objects.filter(student=student).latest('date_report_generation')
        latest_report.is_email_sent = True
        latest_report.save()

    except Exception as e:
        print(f"❌ Failed to send email: {e}")