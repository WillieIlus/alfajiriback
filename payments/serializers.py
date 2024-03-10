from rest_framework import serializers
from .models import Transaction, MpesaPaymentResponse

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'transaction_no',
            'phone_number',
            'checkout_request_id',
            'reference',
            'description',
            'amount',
            'status',
            'receipt_no',
            'created',
            'ip',
        )

class MpesaPaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPaymentResponse
        fields = (
            'merchant_request_id',
            'checkout_request_id',
            'response_code',
            'response_description',
            'customer_message',
        )