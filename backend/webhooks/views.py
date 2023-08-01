from rest_framework.response import Response
from rest_framework import status
from .models import CartAndCheckoutInfo, CheckoutReminderInfo
# from shops.models import Shops
# import shopify
# import requests
import hmac
import hashlib
import base64
from decouple import config
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import datetime
from backend.celery import app
import json

# def create_session_object(request,shop):
#     shopify.Session.setup(api_key = config('SHOPIFY_API_KEY'),secret = config('SHOPIFY_SECRET_KEY'))
#     session = shopify.Session(shop)
#     scope = config("SCOPE").split(",")
#     permission_url = session.create_permission_url(scope=scope)
#     access_token = session.request_token(request.GET)
#     access_scopes = session.access_scopes
#     store_shop_information(access_token,access_scopes,shop)
#     return session

# def store_shop_information(access_token, access_scopes, shop):
#     shop_record = Shops.objects.get_or_create(shopify_domain=shop)[0]
#     shop_record.shopify_token = access_token
#     shop_record.access_scopes = access_scopes

#     shop_record.save()

# def get_session_object(request,shop):
#     queryset = Shops.objects.all().filter(shopify_domain = shop)
#     session = ''
#     if len(queryset) == 0:
#         session = create_session_object(request,shop)
#     else:
#         session = shopify.Session(shop,queryset[0].shopify_token)

#     return session

def verify_webhook(data, hmac_header):
    digest = hmac.new(config('SHARED_SECRET').encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)
    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))

def creationOfCart(request):
    payload = request.body
    verified = verify_webhook(payload,request.headers.get('X-Shopify-Hmac-SHA256'))

    if verified:
        datetime_object = datetime.strptime(payload['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        obj = CartAndCheckoutInfo.objects.create(
            cart_id = payload['id'],
            cart_token = payload['token'],
            cart_created = True,
            cart_creation_time = datetime_object,
            order_created = False
        )
        obj.save()

        timings_object = CheckoutReminderInfo(
            cart = obj,
        )
        timings_object.save()

        schedule_reminder_mail(obj, timings_object.t1)
        schedule_reminder_mail(obj, timings_object.t2)
        schedule_reminder_mail(obj, timings_object.t3)

        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

def updationOfCart(request):
    payload = request.body
    verified = verify_webhook(payload,request.headers.get('X-Shopify-Hmac-SHA256'))
    if verified:
        obj = CartAndCheckoutInfo.objects.get(cart_id = payload['id'])
        obj.cart_updation_time = payload['updated_at']
        cancel_scheduled_mails(obj)
        timings_object = CheckoutReminderInfo.objects.get(cart = obj)
        schedule_reminder_mail(obj, timings_object.t1)
        schedule_reminder_mail(obj, timings_object.t2)
        schedule_reminder_mail(obj, timings_object.t3)
        return Response(status=status.HTTP_202_ACCEPTED)

    return Response(status = status.HTTP_400_BAD_REQUEST)

def creationOfOrder(request):
    payload = request.body
    verified = verify_webhook(payload,request.headers.get('X-Shopify-Hmac-SHA256'))
    if verified:
        obj = CartAndCheckoutInfo.objects.get(payload['cart_id'])
        obj.order_created = True
        cancel_scheduled_mails(obj)
        return Response(status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

def schedule_reminder_mail(obj,schedule_time):
    time_obj = obj.updated_at or obj.created_at
    schedule1, created1 = CrontabSchedule.objects.get_or_create(
        hour = (time_obj.hour + schedule_time.t1).hour, 
        minute = (time_obj.minute + schedule_time.t1).minute
    )
    PeriodicTask.objects.create(
        crontab = schedule1,
        task = "webhooks.tasks.send_email",
        name = obj.cart_id +"-"+ str(schedule_time.t1),
        args = json.dumps({"cart_id" : obj.cart_id}),
        one_off = True,
        expires = datetime.datetime.now() + schedule_time.t1
    )
    return "Done"

def cancel_scheduled_mails(obj):
    for key in app.conf.beat_schedule.keys():
        if obj.cart_id in key:
            del app.conf.beat_schedule[key]