from django.urls import path
from .views import creationOfCart,creationOfCheckout,updationOfCart, sendEmail

urlpatterns = [
    path('create_cart/',creationOfCart),
    path('update_cart/',updationOfCart),
    path('create_checkout/',creationOfCheckout),
    path('sendemail/',sendEmail),
]