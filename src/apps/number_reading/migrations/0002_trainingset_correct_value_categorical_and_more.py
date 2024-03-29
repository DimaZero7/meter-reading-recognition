# Generated by Django 5.0.3 on 2024-03-28 12:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("number_reading", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingset",
            name="correct_value_categorical",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.IntegerField(), size=None
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="correct value categorical",
            ),
        ),
        migrations.AlterField(
            model_name="trainingset",
            name="type",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "training data"), (1, "testing data"), (2, "validation data")],
                default=0,
                verbose_name="type",
            ),
        ),
    ]
