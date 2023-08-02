from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from backend import settings
from .models import CheckoutReminderInfo, ReminderMessages

@shared_task(bind = True)
def send_email(self,data,email):
    if email:
        cart_token = data
        obj = CheckoutReminderInfo.objects.get(cart_id = cart_token)
        message = ""
        if  obj.first_reminder_sent == False:
            obj.first_reminder_sent = True
            message = "First reminder sent"
        elif obj.second_reminder_sent == False:
            obj.second_reminder_sent = True
            message = "Second reminder sent"
        else:
            obj.third_reminder_sent = True
            message = "Third reminder sent"
        reminder_object = ReminderMessages.objects.create(
            cart_token = cart_token,
            message = message
        )
        reminder_object.save()

        mail_subject = "Hey there! Don't forget to checkout the items in your cart!"
        message = "Have a look at them"
        mail_html = render_to_string("main-body.html")
        to_email = "sonawat.1@iitj.ac.in"
        send_mail(
            subject = mail_subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [to_email],
            html_message = mail_html
        )
        return "Done"
    return "No Email id"