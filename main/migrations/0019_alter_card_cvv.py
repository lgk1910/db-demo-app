# Generated by Django 3.2.9 on 2021-11-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_card_cvv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.IntegerField(),
        ),
    ]
