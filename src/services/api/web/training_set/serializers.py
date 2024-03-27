from rest_framework import serializers

from apps.number_reading.models import TrainingSet


class TrainingSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSet
        fields = ("image", "correct_value")
