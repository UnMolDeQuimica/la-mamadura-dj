from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    FormView,
    UpdateView,
    TemplateView,
    View,
)
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from la_mamadura.training.forms import CreateExcerciseRecordForm
from la_mamadura.training.forms import CreateExcerciseRecordFromTrainingForm
from la_mamadura.training.forms import CreateExerciseForm
from la_mamadura.training.forms import CreateTrainingRecordForm
from la_mamadura.training.forms import UpdateExerciseRecord
from la_mamadura.training.forms import CreateExerciseTemplateForm
from la_mamadura.training.forms import CreateTrainingSessionTemplateForm
from la_mamadura.training.forms import CreateWeightRecordForm
from la_mamadura.training.models import Exercise
from la_mamadura.training.models import ExerciseRecord
from la_mamadura.training.models import TrainingSessionRecord
from la_mamadura.training.models import ExerciseTemplate
from la_mamadura.training.models import TrainingSessionTemplate
from la_mamadura.training.models import Weight


class CreateTrainingSessionRecord(LoginRequiredMixin, CreateView):
    form_class = CreateTrainingRecordForm
    template_name = "training/session_record_form.html"
    success_url = reverse_lazy("training:training_records_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TrainingSessionsRecordsList(LoginRequiredMixin, ListView):
    template_name = "training/sessions_records.html"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            msg = f"User {self.user} not found."
            raise Http404(msg)

        return TrainingSessionRecord.objects.filter(
            user__pk=self.request.user.pk,
        ).order_by("-date")

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["entries"] = self.get_queryset()

        return context


class CreateExerciseRecordFromTrainingSession(LoginRequiredMixin, CreateView):
    form_class = CreateExcerciseRecordFromTrainingForm
    template_name = "training/exercise_record_from_training_form.html"

    def get_success_url(self):
        return reverse(
            "training:training_records_create_exercise",
            kwargs={"id": self.training.id},
        )

    def dispatch(self, request, *args, **kwargs):
        self.training = get_object_or_404(TrainingSessionRecord, id=kwargs.get("id"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["training"] = self.training
        exercice_records = self.training.exercise_record.all()
        exercises = {}
        for exercise_record in exercice_records:
            exercise = exercise_record.exercise
            e_record = exercises.get(exercise)
            if not e_record:
                exercises[exercise] = {
                    "n_entries": 1,
                    "entries": [exercise_record],
                }
            else:
                exercises[exercise]["n_entries"] += 1
                exercises[exercise]["entries"].append(exercise_record)

        for exercise in exercises.values():
            status = "pending"
            entries_values = []
            for entry in exercise["entries"]:
                entries_values.append(entry.load * entry.repetitions)

            if any(entries_values):
                status = "started"

            if all(entries_values):
                status = "finished"

            exercise["status"] = status

        context["exercises"] = exercises
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date = self.training.date
        form.instance.training_session = self.training
        return super().form_valid(form)


class CreateExcerciseRecord(LoginRequiredMixin, CreateView):
    # Not being used, not finishing it now.
    form_class = CreateExcerciseRecordForm
    template_name = "training/exercise_record_form.html"

    def get_form(self):
        form = super().get_form()
        form.fields["training_session"].queryset = TrainingSessionRecord.objects.filter(
            user=self.request.user,
        ).order_by("-date")
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return super().get_success_url()


class ExerciseRecordsGraph(LoginRequiredMixin, ListView):
    template_name = "training/exercise_records.html"

    def dispatch(self, request, *args, **kwargs):
        self.exercise = get_object_or_404(Exercise, id=kwargs.get("id"))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            msg = f"User {self.user} not found."
            raise Http404(msg)

        if not self.exercise:
            msg = f"Exercise {self.exercise} not found."
            raise Http404(msg)

        return ExerciseRecord.objects.filter(
            user__pk=self.request.user.pk,
            exercise__id=self.exercise.id,
        ).order_by("date")

    def get_context_data(self, *, object_list=..., **kwargs):
        qs = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["exercise"] = self.exercise.name
        context["entries"] = qs
        context["units"] = self.exercise.load_units
        context["exercises"] = Exercise.objects.all()
        context["pr"] = qs.aggregate(Max("load")).get("load__max") if qs.exists() else 0

        return context


class ExerciseRecordUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateExerciseRecord
    template_name = "training/update_exercise_record_form.html"

    def get_object(self, queryset=None):
        return self.exercise_record

    def dispatch(self, request, *args, **kwargs):
        self.exercise_record = get_object_or_404(ExerciseRecord, pk=kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            "training:training_records_create_exercise",
            kwargs={"id": self.exercise_record.training_session.pk},
        )


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CreateExerciseForm
    template_name = "training/exercise_update_form.html"

    def get_object(self, queryset=None):
        return self.exercise

    def dispatch(self, request, *args, **kwargs):
        self.exercise = get_object_or_404(Exercise, pk=kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            "training:exercises_update",
            kwargs={"pk": self.exercise.pk},
        )


class ExercisesListView(LoginRequiredMixin, ListView):
    template_name = "training/exercises_list.html"

    def get_queryset(self):
        return Exercise.objects.all().order_by("name")

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["entries"] = self.get_queryset()

        return context


class CreateExerciseView(LoginRequiredMixin, CreateView):
    form_class = CreateExerciseForm
    template_name = "training/exercise_create_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, message=_("Exercise created successfully!"))

        return response

    def get_success_url(self):
        return reverse("training:exercises_update", kwargs={"pk": self.object.pk})


class CreateExerciseTemplate(LoginRequiredMixin, CreateView):
    form_class = CreateExerciseTemplateForm
    template_name = "training/exercise_template_create_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, message=_("Exercise Template created succesfully!")
        )

        return response

    def get_success_url(self):
        return reverse(
            "training:training_session_templates_update",
            kwargs={"pk": self.object.template.pk},
        )


class UpdateExerciseTemplate(LoginRequiredMixin, UpdateView):
    form_class = CreateExerciseTemplateForm
    template_name = "training/exercise_template_create_form.html"
    model = ExerciseTemplate

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, message=_("Exercise Template updated succesfully!")
        )

        return response

    def get_success_url(self):
        return reverse(
            "training:exercise_templates_update", kwargs={"pk": self.object.pk}
        )


class ListExerciseTemplate(LoginRequiredMixin, ListView):
    template_name = "training/exercise_template_list.html"
    model = ExerciseTemplate
    context_object_name = "exercise_templates"


class CreateTrainingSessionTemplate(LoginRequiredMixin, CreateView):
    form_class = CreateTrainingSessionTemplateForm
    template_name = "training/training_template_create_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, message=_("Exercise Template created succesfully!")
        )

        return response

    def get_success_url(self):
        return reverse(
            "training:training_session_templates_update", kwargs={"pk": self.object.pk}
        )


class UpdateTrainingSessionTemplate(LoginRequiredMixin, UpdateView):
    form_class = CreateTrainingSessionTemplateForm
    template_name = "training/training_template_update_form.html"
    model = TrainingSessionTemplate
    context_object_name = "training_template"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, message=_("Training Session Template updated succesfully!")
        )

        return response

    def get_success_url(self):
        return reverse(
            "training:training_session_templates_update", kwargs={"pk": self.object.pk}
        )


class ListTrainingSessionTemplate(LoginRequiredMixin, ListView):
    template_name = "training/training_template_list.html"
    model = TrainingSessionTemplate
    context_object_name = "training_templates"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(user__isnull=True) | Q(user__id=self.request.user.id))


class TemplatesView(LoginRequiredMixin, TemplateView):
    template_name = "training/templates.html"


class CreateTrainingRecordFromTemplate(LoginRequiredMixin, FormView):
    template_name = "training/create_training_from_template.html"

    def create_training_from_template(self):
        training_session = TrainingSessionRecord.objects.create(user=self.request.user)

        return training_session

    def create_exercise_records_from_template(
        self, template: TrainingSessionTemplate, training_session: TrainingSessionRecord
    ):
        for exercise in template.exercise_template.all():
            for i in range(exercise.sets):
                ExerciseRecord.objects.create(
                    user=training_session.user,
                    exercise=exercise.exercise,
                    repetitions=0,
                    load=0,
                    training_session=training_session,
                )

    def get_form(self):
        form_class = CreateTrainingSessionTemplateForm

    template_name = "training/training_template_create_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, message=_("Exercise Template created succesfully!")
        )

        return response

    def get_success_url(self):
        return reverse(
            "training:training_session_templates_update", kwargs={"pk": self.object.pk}
        )
        self.create_exercise_records_from_template(
            template=template, training_session=training_session
        )
        self.training_session_id = training_session.id
        messages.success(
            self.request, message=_("Training Session created succesfully!")
        )

        return super().form_valid(form)


class GetOrCreateLatestTrainigRecord(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)
        qs = (
            TrainingSessionRecord.objects.filter(date__in=[today, yesterday])
            .order_by("date")
            .last()
        )
        if not qs:
            qs = TrainingSessionRecord.objects.create(user=user)

        return redirect(
            reverse("training:training_records_create_exercise", kwargs={"id": qs.id}),
        )


class WeightRecordGraph(LoginRequiredMixin, ListView):
    template_name = "training/weight_records.html"

    def get_queryset(self):
        return Weight.objects.filter(
            user__pk=self.request.user.pk,
        ).order_by("date")

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["entries"] = self.get_queryset()

        return context


class CreateWeightRecord(LoginRequiredMixin, CreateView):
    form_class = CreateWeightRecordForm
    template_name = "training/create_weight_record_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, message=_("Weight record created succesfully!"))

        return response

    def get_success_url(self):
        return reverse("training:weight_record_graph")


class UpdateWeightRecord(LoginRequiredMixin, UpdateView):
    form_class = CreateWeightRecordForm
    template_name = "training/create_weight_record_form.html"
    model = Weight
    
    def get(self, request, *args, **kwargs):
        print(self)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, message=_("Weight record created succesfully!"))

        return response

    def get_success_url(self):
        return reverse("training:weight_record_graph")
