from django.db import models
import datetime
# Create your models here.

class CartAndCheckoutInfo(models.Model):
    cart_id = models.CharField(max_length = 32, primary_key = True)
    cart_token = models.CharField(max_length = 32)
    cart_created = models.BooleanField(default = False)
    cart_creation_time = models.DateTimeField(default = datetime.datetime.now())
    cart_updation_time = models.DateTimeField(null = True)
    order_created = models.BooleanField(default = False, null = True)

class CheckoutReminderInfo(models.Model):
    cart = models.ForeignKey(CartAndCheckoutInfo, on_delete = models.CASCADE,related_name="timings")
    t1 = models.DurationField(default = datetime.timedelta(minutes = 30))
    first_reminder_sent = models.BooleanField(default = False, null = True)
    t2 = models.DurationField(default = datetime.timedelta(days = 1))
    second_reminder_sent = models.BooleanField(default = False, null = True)
    t3 = models.DurationField(default = datetime.timedelta(days = 3))
    third_reminder_sent = models.BooleanField(default = False, null = True)