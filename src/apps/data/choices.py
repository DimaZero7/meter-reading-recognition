from django.db import models
from django.utils.translation import gettext_lazy as _


class TrainingType(models.IntegerChoices):
    TEACH = 0, _("teaching data")
    TEST = 1, _("testing data")
    VALIDATE = 2, _("validation data")


class TrainingElementPositionType(models.IntegerChoices):
    START = 0, _("start")
    MIDDLE = 1, _("middle")
    END = 2, _("end")


class TrainingElementMeterType(models.IntegerChoices):
    MERCURY_201 = 0, _("mercury 201")


class TrainingAugmentationType(models.IntegerChoices):
    TEACH = 0, _("teaching data")
