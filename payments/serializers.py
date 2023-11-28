import stripe
from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    pay_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

    def get_pay_status(self, instance):
        payment_id = instance.id_payment
        pay_retrieve = stripe.PaymentIntent.retrieve(payment_id)

        return pay_retrieve.status
