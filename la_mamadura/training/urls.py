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
from .views import CreateExerciseTemplate
from .views import UpdateExerciseTemplate
from .views import CreateTrainingSessionTemplate
from .views import UpdateTrainingSessionTemplate, GetOrCreateLatestTrainigRecord

from . import views

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
    path(
        "exercise-templates/create",
        view=CreateExerciseTemplate.as_view(),
        name="exercise_templates_create",
    ),
    path(
        "exercise-templates/<int:pk>",
        view=UpdateExerciseTemplate.as_view(),
        name="exercise_templates_update",
    ),
    path(
        "exercise-templates/",
        view=views.ListExerciseTemplate.as_view(),
        name="exercise_templates_list",
    ),
    path(
        "training-templates/create",
        view=CreateTrainingSessionTemplate.as_view(),
        name="training_session_templates_create",
    ),
    path(
        "training-templates/<int:pk>",
        view=UpdateTrainingSessionTemplate.as_view(),
        name="training_session_templates_update",
    ),
    path(
        "training-templates/",
        view=views.ListTrainingSessionTemplate.as_view(),
        name="training_session_templates_list",
    ),
    path(
        "templates/",
        view=views.TemplatesView.as_view(),
        name="templates",
    ),
    path(
        "training-from-template/",
        view=views.CreateTrainingRecordFromTemplate.as_view(),
        name="training_from_template",
    ),
    path(
        "last-training/",
        view=views.GetOrCreateLatestTrainigRecord.as_view(),
        name="get_last_training",
    ),
    path(
        "weight/create/",
        view=views.CreateWeightRecord.as_view(),
        name="create_weight_record",
    ),
    path(
        "weight/",
        view=views.WeightRecordGraph.as_view(),
        name="weight_record_graph",
    ),
    path(
        "weight/<int:pk>/",
        view=views.UpdateWeightRecord.as_view(),
        name="weight_record_update",
    ),
]
