from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import CartAndCheckoutInfo
from shops.models import Shops
import shopify
import requests
import hmac
import hashlib
import base64
from .tasks import send_email
from decouple import config
from django.http import HttpResponse

def create_session_object(request,shop):
    shopify.Session.setup(api_key = config('SHOPIFY_API_KEY'),secret = config('SHOPIFY_SECRET_KEY'))
    session = shopify.Session(shop)
    scope = config("SCOPE").split(",")
    permission_url = session.create_permission_url(scope=scope)
    access_token = session.request_token(request.GET)
    access_scopes = session.access_scopes
    store_shop_information(access_token,access_scopes,shop)
    return session

def store_shop_information(access_token, access_scopes, shop):
    shop_record = Shops.objects.get_or_create(shopify_domain=shop)[0]
    shop_record.shopify_token = access_token
    shop_record.access_scopes = access_scopes

    shop_record.save()

def get_session_object(request,shop):
    queryset = Shops.objects.all().filter(shopify_domain = shop)
    session = ''
    if len(queryset) == 0:
        session = create_session_object(request,shop)
    else:
        session = shopify.Session(shop,queryset[0].shopify_token)

    return session

def verify_webhook(data, hmac_header):
    digest = hmac.new(config('SHARED_SECRET').encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)
    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))

def creationOfCart(request):
    shop = request.GET.get("shop") or config('SHOP')
    payload = request.body
    verified = verify_webhook(payload,request.headers.get('X-Shopify-Hmac-SHA256'))
    if verified:
        obj = CartAndCheckoutInfo.objects.create(
            cart_id = payload['id'],
            cart_token = payload['token'],
            cart_created = True,
            cart_creation_time = payload['created_at'],
        )
        obj.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

def updationOfCart(request):
    shop = request.GET.get("shop") or config('SHOP')
    payload = request.body
    verified = verify_webhook(payload,request.headers.get('X-Shopify-Hmac-SHA256'))
    if verified:
        obj = CartAndCheckoutInfo.objects.get(cart_id = payload['id'])
        obj.cart_updation_time = payload['updated_at']
        return Response(status=status.HTTP_202_ACCEPTED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

def creationOfOrder(request):
    shop = request.GET.get("shop") or config('SHOP')
    payload = request.body
    verified = verify_webhook(payload,request.headers.get('X-Shopify-Hmac-SHA256'))
    if verified:
        return Response(status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

def sendEmail(request):   # Doubtful how you will do it
    send_email.delay()
    return HttpResponse("Done")