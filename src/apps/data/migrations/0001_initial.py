# Generated by Django 5.0.4 on 2024-05-06 12:13

import apps.common.services
import django.contrib.postgres.fields
import functools
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Training",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_timestamp",
                    models.DateTimeField(
                        auto_now=True, verbose_name="updated at"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=functools.partial(
                            apps.common.services.upload_file_handler_path,
                            *("images/training",),
                            **{}
                        ),
                        verbose_name="image",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "teaching data"),
                            (1, "testing data"),
                            (2, "validation data"),
                        ],
                        default=0,
                        verbose_name="type",
                    ),
                ),
                (
                    "correct_value",
                    models.CharField(verbose_name="correct value"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TrainingElement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_timestamp",
                    models.DateTimeField(
                        auto_now=True, verbose_name="updated at"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=functools.partial(
                            apps.common.services.upload_file_handler_path,
                            *("images/training_element",),
                            **{}
                        ),
                        verbose_name="image",
                    ),
                ),
                (
                    "number_type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "integer"), (1, "float")],
                        verbose_name="part",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "mercury 201")],
                        verbose_name="type",
                    ),
                ),
                (
                    "correct_value",
                    models.CharField(verbose_name="correct value"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TrainingSetAugmentation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_timestamp",
                    models.DateTimeField(
                        auto_now=True, verbose_name="updated at"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=functools.partial(
                            apps.common.services.upload_file_handler_path,
                            *("images/training_augmentation",),
                            **{}
                        ),
                        verbose_name="image",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "mercury 201")],
                        verbose_name="type",
                    ),
                ),
                (
                    "correct_value",
                    models.CharField(verbose_name="correct value"),
                ),
                (
                    "training_element_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.IntegerField(),
                            size=None,
                        ),
                        size=None,
                        unique=True,
                        verbose_name="correct value categorical",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
