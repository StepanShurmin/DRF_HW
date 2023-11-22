import os

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework.filters import OrderingFilter
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsOwner, IsModerator
from payments.models import Payment
from payments.serializers import PaymentSerializer

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payment_id = request.data.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id)

        try:
            stripe.Charge.create(
                amount=int(Payment.price),
                currency="usd",
                source=request.data.get("stripeToken"),
                description=f"Payment for {payment.user}"
            )
            return Response({"message": "Успешно"}, status=status.HTTP_201_CREATED)
        except stripe.error.CardError as e:
            return Response({"message": e.user_message}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError:
            return Response({"message": "Что-то пошло не так. Пожалуйста, попробуйте еще раз позже."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
