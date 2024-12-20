# Generated by Django 5.0.4 on 2024-10-22 11:40

import apps.common.services
import functools
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("neural_net", "0005_neuralmodel_structure_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="neuralversion",
            name="tflite_model",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=functools.partial(
                    apps.common.services.upload_file_handler_path,
                    *("neural_net/tflite_models",),
                    **{}
                ),
            ),
        ),
    ]
