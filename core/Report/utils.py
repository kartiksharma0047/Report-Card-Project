from django.core.mail import send_mail
from django.conf import settings
def send_email():
    subject="Testing Email from django server"
    message="Hi there! This is just a practice email used for nothing"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=["kartiksharma55109@gmail.com"]
    send_email(subject,message,from_email,recipient_list)