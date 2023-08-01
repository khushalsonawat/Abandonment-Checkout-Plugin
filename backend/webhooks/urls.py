from django.urls import path
from .views import creationOfCart,creationOfOrder,updationOfCart, schedule_reminder_mail, viewReminderMessages

urlpatterns = [
    path('create_cart/',creationOfCart),
    path('update_cart/',updationOfCart),
    path('create_order/',creationOfOrder),
    path('view_reminder_messages/',viewReminderMessages),
]