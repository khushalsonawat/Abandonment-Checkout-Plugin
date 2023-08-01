from celery import shared_task
from django.core.mail import send_mail
from backend import settings
# from django.

@shared_task(bind = True)
def send_email(self):
    mail_subject = "Hi! Celery Testing"
    message = "Hooray! I made it work!"
    to_email = "khushalsonawat@gmail.com"
    send_mail(
        subject = mail_subject,
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [to_email],
    )
    return "Done"