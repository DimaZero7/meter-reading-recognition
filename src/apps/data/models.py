from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.common.models import TimeStampedAbstractModel
from django.utils.translation import gettext_lazy as _

from apps.common.services import prefix_based_upload_handler
from apps.data.choices import TrainingType, TrainingElementPositionType, TrainingElementMeterType, \
    TrainingAugmentationType


class Training(TimeStampedAbstractModel):
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
        choices=TrainingType.choices,
        default=TrainingType.TEACH.value,
    )
    correct_value = models.FloatField(verbose_name=_("correct value"))

    def __str__(self):
        return f"{self.id}"


class TrainingElement(TimeStampedAbstractModel):
    """
    Image chunks for generating augmented data
    """
    # Main fields
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=prefix_based_upload_handler("images/training_element"),
    )
    number_type = models.PositiveSmallIntegerField(
        verbose_name=_("part"),
        choices=TrainingElementPositionType.choices,
    )
    meter_type = models.PositiveSmallIntegerField(
        verbose_name=_("type"),
        choices=TrainingElementMeterType.choices,
    )
    correct_value = models.CharField(verbose_name=_("correct value"))

    def __str__(self):
        return f"{self.id}"


class TrainingAugmentation(TimeStampedAbstractModel):
    # Main fields
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=prefix_based_upload_handler("images/training_augmentation"),
    )
    meter_type = models.PositiveSmallIntegerField(
        verbose_name=_("type"),
        choices=TrainingElementMeterType.choices,
    )
    correct_value = models.FloatField(verbose_name=_("correct value"))
    training_element_ids = ArrayField(
        verbose_name=_("correct value categorical"),
        base_field=ArrayField(models.IntegerField()),
        unique=False
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("type"),
        choices=TrainingAugmentationType.choices,
        default=TrainingAugmentationType.TEACH.value,
    )

    def __str__(self):
        return f"{self.id}"
