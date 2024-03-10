from django.urls import path

from .views import initiate_payment_view, check_payment, mpesa_callback_view

app_name = 'payments'

urlpatterns = [
    path('', initiate_payment_view, name='index'),
    path('initiate-payment/', initiate_payment_view, name='initiate-payment'),
    path('check_payment/<str:checkout_request_id>/', check_payment, name='check_payment'),
    path('callback/', mpesa_callback_view, name='mpesa-callback'),
]