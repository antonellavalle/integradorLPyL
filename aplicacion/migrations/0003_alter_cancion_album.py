# Generated by Django 5.0.6 on 2024-07-02 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0002_usuario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancion',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplicacion.album'),
        ),
    ]
