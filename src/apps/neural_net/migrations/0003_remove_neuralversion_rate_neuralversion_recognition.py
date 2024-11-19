# Generated by Django 5.0.4 on 2024-05-22 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "neural_net",
            "0002_rename_recognition_rate_neuralversion_rate",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="neuralversion",
            name="rate",
        ),
        migrations.AddField(
            model_name="neuralversion",
            name="recognition",
            field=models.JSONField(
                default=1, verbose_name="recognition"
            ),
            preserve_default=False,
        ),
    ]
