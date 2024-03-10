from django.contrib import admin

from .models import MpesaPaymentResponse, Transaction


@admin.register(MpesaPaymentResponse)
class MpesaPaymentResponseAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'merchant_request_id', 'checkout_request_id', 'response_code', 'customer_message')
    list_display_links = ('id', 'merchant_request_id',)


admin.site.register(Transaction)
