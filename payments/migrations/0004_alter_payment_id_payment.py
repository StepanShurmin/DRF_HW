# Generated by Django 4.2.7 on 2023-11-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_payment_id_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='id_payment',
            field=models.PositiveIntegerField(auto_created=True, null=True, verbose_name='id-платежа'),
        ),
    ]