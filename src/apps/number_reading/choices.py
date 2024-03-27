from django.db import models
from django.utils.translation import gettext_lazy as _


class TrainingSetType(models.IntegerChoices):
    TEACH = 0, _("training data")
    TEST = 1, _("testing data")
    VALIDATE = 2, _("validation data")
