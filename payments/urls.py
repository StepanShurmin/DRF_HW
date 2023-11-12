from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, PaymentUpdateAPIView, \
    PaymentDestroyAPIView

app_name = PaymentsConfig.name


urlpatterns =[
    path('create/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('', PaymentListAPIView.as_view(), name='list_payment'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='get_payment'),
    path('update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='update_payment'),
    path('delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='delete_payment'),
]