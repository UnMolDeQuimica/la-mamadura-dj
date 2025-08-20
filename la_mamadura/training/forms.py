from django.forms import ModelForm
from django.forms import TextInput
from django.forms import ModelChoiceField
from django.forms import Form
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


from la_mamadura.training.models import Exercise
from la_mamadura.training.models import ExerciseRecord
from la_mamadura.training.models import TrainingSessionRecord
from la_mamadura.training.models import ExerciseTemplate
from la_mamadura.training.models import TrainingSessionTemplate


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


class CreateExerciseTemplateForm(ModelForm):
    class Meta:
        model = ExerciseTemplate
        fields = "__all__"


class CreateTrainingSessionTemplateForm(ModelForm):
    class Meta:
        model = TrainingSessionTemplate
        fields = ["name"]


class CreateTrainingFromTemplateForm(Form):
    template = ModelChoiceField(
        queryset=TrainingSessionTemplate.objects.all(), label=_("Choose a Template")
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["template"].queryset = TrainingSessionTemplate.objects.filter(
                Q(user__isnull=True) | Q(user__id=user.id)
            )
