from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'course', 'lesson')
    list_filter = ('course', 'lesson')
