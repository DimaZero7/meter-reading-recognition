from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.services import prefix_based_upload_handler
from apps.number_reading.choices import TrainingSetType


class TrainingSet(models.Model):
    """
    Data for neural network training
    Original data only, no augmented data
    """

    # Main fields
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=prefix_based_upload_handler("images/training"),
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("type"),
        choices=TrainingSetType.choices,
        default=TrainingSetType.TEACH.value,
    )
    correct_value = models.FloatField(verbose_name=_("correct value"))

    # Additional fields
    correct_value_categorical = ArrayField(
        verbose_name=_("correct value categorical"),
        base_field=ArrayField(models.IntegerField()),
        null=True,
        blank=True,
    )
    image_resized = models.ImageField(
        verbose_name=_("image resized"),
        upload_to=prefix_based_upload_handler("images/training_resized"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}"
