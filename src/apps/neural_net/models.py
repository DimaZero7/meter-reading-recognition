from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.services import prefix_based_upload_handler


class NeuralModel(models.Model):
    # Main fields
    name = models.CharField(verbose_name=_("name"), max_length=128, unique=True)
    structure = models.JSONField(verbose_name=_("structure"))


class NeuralVersion(models.Model):
    # Foreign keys
    neural_model = models.ForeignKey(
        NeuralModel,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name=_("neural model"),
    )

    # Main fields
    version = models.IntegerField(verbose_name=_("version"))
    changes = models.TextField(verbose_name=_("changes"))
    model = models.FileField(upload_to=prefix_based_upload_handler('neural_net/models'))
    tflite_model = models.FileField(upload_to=prefix_based_upload_handler('neural_net/tflite_models'), null=True, blank=True)
    stats = models.JSONField(verbose_name=_("stats"))
