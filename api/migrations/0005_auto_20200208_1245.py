# Generated by Django 2.2 on 2020-02-08 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200208_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(blank=True, choices=[('Unidades', 'Unidad'), ('Kilogramos', 'Kilogramos'), ('Gramos', 'Gramos'), ('Litros', 'Litros'), ('Mili-Litros', 'Mili-Litros')], default='Unidades', max_length=20, null=True),
        ),
    ]
