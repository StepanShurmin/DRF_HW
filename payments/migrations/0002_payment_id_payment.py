# Generated by Django 4.2.7 on 2023-11-24 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='id_payment',
            field=models.CharField(blank=True, null=True, verbose_name='id-платежа'),
        ),
    ]
