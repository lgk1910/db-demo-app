# Generated by Django 3.2.9 on 2021-11-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_rename_creditcard_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='balance',
            field=models.IntegerField(default=200000),
        ),
        migrations.AddField(
            model_name='card',
            name='cvv',
            field=models.IntegerField(default=234),
            preserve_default=False,
        ),
    ]
