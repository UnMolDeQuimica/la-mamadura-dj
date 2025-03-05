from django.forms import ModelForm
from django.forms import TextInput

from la_mamadura.training.models import ExerciseRecord, TrainingSessionRecord, Exercise


class CreateTrainingRecordForm(ModelForm):
    class Meta:
        model = TrainingSessionRecord
        exclude = ["user"]
        widgets = {
            "date": TextInput(attrs={"type": "date"}),
        }


class CreateExcerciseRecordForm(ModelForm):
    class Meta:
        model = ExerciseRecord
        exclude = ["user"]
        widgets = {
            "date": TextInput(attrs={"type": "date"}),
        }


class CreateExcerciseRecordFromTrainingForm(ModelForm):
    class Meta:
        model = ExerciseRecord
        exclude = ["user", "training_session", "date"]
        widgets = {
            "date": TextInput(attrs={"type": "date"}),
        }


class UpdateExerciseRecord(ModelForm):
    class Meta:
        model = ExerciseRecord
        exclude = ["user"]
        widgets = {
            "date": TextInput(attrs={"type": "date"}),
        }


class CreateExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"
