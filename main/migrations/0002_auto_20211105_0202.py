# Generated by Django 3.2.9 on 2021-11-04 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='transactioninfo',
            name='customer_id',
        ),
    ]
