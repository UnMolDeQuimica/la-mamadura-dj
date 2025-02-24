from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from la_mamadura.training.forms import CreateExcerciseRecordForm
from la_mamadura.training.forms import CreateExcerciseRecordFromTrainingForm
from la_mamadura.training.forms import CreateTrainingRecordForm
from la_mamadura.training.forms import UpdateExerciseRecord
from la_mamadura.training.models import Exercise
from la_mamadura.training.models import ExerciseRecord
from la_mamadura.training.models import TrainingSessionRecord


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

        return get_list_or_404(
            TrainingSessionRecord.objects.order_by("-date"),
            user__pk=self.request.user.pk,
        )

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

        return get_list_or_404(
            ExerciseRecord.objects.order_by("date"),
            user__pk=self.request.user.pk,
            exercise__id=self.exercise.id,
        )

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["exercise"] = self.exercise.name
        context["entries"] = self.get_queryset()
        context["units"] = self.exercise.load_units

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
            "training:exercise_record_update", kwargs={"pk": self.exercise_record.pkc},
        )
