from celery import shared_task
from django.core.mail import send_mail
from backend import settings
from .models import CartAndCheckoutInfo, CheckoutReminderInfo, ReminderMessages
import json
# from django.

@shared_task(bind = True)
def send_email(self,data):
    cart_id = json.loads(data)["cart_id"]
    obj = CheckoutReminderInfo.objects.get(cart_id = cart_id)
    message = ""
    if not obj.first_reminder_sent:
        obj.first_reminder_sent = True
        message = "First reminder sent to for cart id {}".format(cart_id)
    elif not obj.second_reminder_sent:
        obj.second_reminder_sent = True
        message = "Second reminder sent to for cart id {}".format(cart_id)
    else:
        obj.third_reminder_sent = True
        message = "Third reminder sent to for cart id {}".format(cart_id)
    reminder_object = ReminderMessages.object.create(
        cart_id = cart_id,
        message = message
    )
    reminder_object.save()

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