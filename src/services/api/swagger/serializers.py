from rest_framework import serializers

from apps.users.choices import ActiveProgram, TrainingTime
from apps.users.validators import number_of_sessions_validator
from services.api.mobile.exercises.serializers import ExerciseSerializer
from services.api.mobile.playlists.serializers import PlaylistSerializer


class DanceCreateSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(default=False)
    number_of_sessions = serializers.IntegerField(
        validators=[number_of_sessions_validator]
    )
    training_time = serializers.ChoiceField(choices=TrainingTime.choices)
    dance_id = serializers.IntegerField()


class ViewedVideoSerializer(serializers.Serializer):
    viewed_time = serializers.IntegerField()


class ExersiceResponseSerializer(serializers.Serializer):
    title = serializers.CharField(default="exercise_1")
    duration = serializers.IntegerField(default=10)
    image = serializers.CharField(default="path/to/image")
    video = serializers.CharField(default="path/to/video")
    is_done = serializers.BooleanField(default=False)
    time_percent = serializers.IntegerField(default=0)
    time_seconds = serializers.IntegerField(default=1)
    order = serializers.IntegerField(default=1)


class ExercisesDaySortedSerializer(serializers.Serializer):
    title = serializers.CharField(default="day 1")
    exercises = ExersiceResponseSerializer(many=True)


class ProgressFieldSerializer(serializers.Serializer):
    percent = serializers.IntegerField(default=1)
    total_days = serializers.IntegerField(default=3)
    current_day = serializers.IntegerField(default=1)
    current_videos_count = serializers.IntegerField(default=4)


class ResponsePlaylistSerializer(PlaylistSerializer):
    progress = ProgressFieldSerializer()


class ResponsePlaylistListSerializer(serializers.Serializer):
    personal = ResponsePlaylistSerializer()
    dance = ResponsePlaylistSerializer()


class ActiveProgramChoiceSerializer(serializers.Serializer):
    active_program = serializers.ChoiceField(choices=ActiveProgram.choices)


class ExerciseDoneSerializer(serializers.Serializer):
    title = serializers.CharField(default="exercise_1")
    duration = serializers.IntegerField(default=10)
    image = serializers.CharField(default="path/to/image")
    video = serializers.CharField(default="path/to/video")
    time_seconds = serializers.IntegerField(default=1)
    order = serializers.IntegerField(default=1)


class DoneExersiceResponseSerializer(serializers.Serializer):
    title = serializers.CharField(default="playlist title")
    exercises = ExerciseDoneSerializer(many=True)


class ExercisesAllSerializer(serializers.Serializer):
    title = serializers.CharField(default="beginner")
    exercises = ExerciseSerializer(many=True)
