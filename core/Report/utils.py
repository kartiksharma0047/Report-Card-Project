from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import os
from django.conf import settings
from django.core.mail import EmailMessage

def render_pdf_from_template(template_src, context, filename):
    html = render_to_string(template_src, context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        path = os.path.join(settings.BASE_DIR, 'Student_Result_pdfs', filename)
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
        from_email="your_email@example.com",
        to=[student.email],
    )
    email.content_subtype = "html"  # 📌 Important to render HTML in body
    email.attach_file(pdf_path)
    email.send()
