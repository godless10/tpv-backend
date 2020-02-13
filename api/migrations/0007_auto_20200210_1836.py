# Generated by Django 2.2 on 2020-02-10 23:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200208_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='tipo_fact',
            field=models.IntegerField(blank=True, choices=[(0, 'Salon pdte. Pago'), (1, 'Salon Pagada'), (2, 'Domicilio pdte. Pago'), (3, 'Domicilio Pagado')], default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
        ),
    ]