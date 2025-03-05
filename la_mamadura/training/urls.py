from django.urls import path

from .views import CreateExcerciseRecord
from .views import CreateExerciseRecordFromTrainingSession
from .views import CreateExerciseView
from .views import CreateTrainingSessionRecord
from .views import ExerciseRecordsGraph
from .views import ExerciseRecordUpdateView
from .views import ExercisesListView
from .views import ExerciseUpdateView
from .views import TrainingSessionsRecordsList

app_name = "training"
urlpatterns = [
    path(
        "exercise-record-graph/<int:id>/",
        view=ExerciseRecordsGraph.as_view(),
        name="exercise_record_graph",
    ),
    path(
        "exercise-record/<int:pk>/",
        view=ExerciseRecordUpdateView.as_view(),
        name="exercise_record_update",
    ),
    path(
        "exercise-record/",
        view=CreateExcerciseRecord.as_view(),
        name="exercise_record_create",
    ),
    path(
        "records/",
        view=TrainingSessionsRecordsList.as_view(),
        name="training_records_list",
    ),
    path(
        "records/create/",
        view=CreateTrainingSessionRecord.as_view(),
        name="training_records_create",
    ),
    path(
        "records/<int:id>/",
        view=CreateExerciseRecordFromTrainingSession.as_view(),
        name="training_records_create_exercise",
    ),
    path(
        "exercises/<int:pk>/",
        view=ExerciseUpdateView.as_view(),
        name="exercises_update",
    ),
    path(
        "exercises/",
        view=ExercisesListView.as_view(),
        name="exercises_list",
    ),
    path(
        "exercises/create/",
        view=CreateExerciseView.as_view(),
        name="exercise_create",
    ),
]
