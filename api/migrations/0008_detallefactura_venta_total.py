# Generated by Django 2.2 on 2020-02-11 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200210_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefactura',
            name='venta_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=1000),
        ),
    ]
