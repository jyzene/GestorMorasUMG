# Generated by Django 5.0.6 on 2025-05-20 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestorMoras', '0002_tipo_cobro_estudiante_cartera'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartera',
            name='Estudiante',
        ),
        migrations.RemoveField(
            model_name='cartera',
            name='Metodo_pago',
        ),
        migrations.RemoveField(
            model_name='cartera',
            name='Status_pago',
        ),
        migrations.RemoveField(
            model_name='cartera',
            name='Tipo_cobro',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='Estatus',
        ),
        migrations.DeleteModel(
            name='Metodo_Pago',
        ),
        migrations.DeleteModel(
            name='Status_Pago',
        ),
        migrations.DeleteModel(
            name='Cartera',
        ),
        migrations.DeleteModel(
            name='Tipo_cobro',
        ),
        migrations.DeleteModel(
            name='Estudiante',
        ),
        migrations.DeleteModel(
            name='Status_Estudiante',
        ),
    ]
