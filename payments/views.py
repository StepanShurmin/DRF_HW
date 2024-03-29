import os

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner, IsModerator
from payments.models import Payment
from payments.serializers import PaymentSerializer

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        payment.save()
        payment_res = self.payment_create()
        serializer.instance.id_payment = payment_res.id
        serializer.instance.save()
        return super().perform_create(serializer)

    def payment_create(self):
        pay = stripe.PaymentIntent.create(
            amount=self.request.data['price'],
            currency="usd",
            automatic_payment_methods={"enabled": True},

        )
        pay.save()
        return pay


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('date',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
