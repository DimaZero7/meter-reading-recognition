# Generated by Django 5.0.4 on 2024-06-11 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("neural_net", "0004_rename_recognition_neuralversion_stats"),
    ]

    operations = [
        migrations.AddField(
            model_name="neuralmodel",
            name="structure",
            field=models.JSONField(
                default=1, verbose_name="structure"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="neuralversion",
            name="neural_model",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="versions",
                to="neural_net.neuralmodel",
                verbose_name="neural model",
            ),
        ),
        migrations.AlterField(
            model_name="neuralversion",
            name="stats",
            field=models.JSONField(verbose_name="stats"),
        ),
    ]