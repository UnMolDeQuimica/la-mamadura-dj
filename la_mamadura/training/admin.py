from django.contrib import admin

from .models import CustomTrainingSession
from .models import Exercise
from .models import ExerciseRecord
from .models import Muscle
from .models import MuscularGroup
from .models import SubMuscle
from .models import TrainingSession
from .models import TrainingSessionRecord


@admin.register(SubMuscle)
class SubMuscleAdmin(admin.ModelAdmin): ...


@admin.register(Muscle)
class MuscleAdmin(admin.ModelAdmin): ...


@admin.register(MuscularGroup)
class MuscularGroupAdmin(admin.ModelAdmin): ...


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin): ...


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin): ...


@admin.register(CustomTrainingSession)
class CustomTrainingSessionAdmin(admin.ModelAdmin): ...


@admin.register(TrainingSessionRecord)
class TrainingSessionRecordAdmin(admin.ModelAdmin): ...


@admin.register(ExerciseRecord)
class ExerciseRecordAdmin(admin.ModelAdmin): ...
