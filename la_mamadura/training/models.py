from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from la_mamadura.users.models import User


class SubMuscle(models.Model):
    """
    Defines a submuscle that belongs to a bigger muscle such
    as the heads of the tryceps.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        unique=True,
    )
    name_es = models.CharField(
        verbose_name=_("Name ES"),
        max_length=255,
        blank=False,
        unique=True,
    )

    image = models.ImageField(verbose_name=_("Image"), blank=True, null=True)

    def __str__(self):
        return self.name


class Muscle(models.Model):
    """
    Defines a muscle such as the tryceps.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        unique=True,
    )
    name_es = models.CharField(
        verbose_name=_("Name ES"),
        max_length=255,
        blank=False,
        unique=True,
    )

    submuscles = models.ManyToManyField(
        SubMuscle,
        related_name="muscle",
        blank=True,
    )
    image = models.ImageField(verbose_name=_("Image"), blank=True, null=True)

    def __str__(self):
        return self.name


class MuscularGroup(models.Model):
    """
    Defines a muscular group such as chest.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        unique=True,
    )
    name_es = models.CharField(
        verbose_name=_("Name ES"),
        max_length=255,
        blank=False,
        unique=True,
    )

    muscles = models.ManyToManyField(Muscle, related_name="muscular_group")
    image = models.ImageField(verbose_name=_("Image"), blank=True, null=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    """
    Defines an exercise such as bench press.
    """

    LOAD_UNITS = (
        ("KG", "kg"),
        ("KM", "km"),
        ("M", "m"),
        ("MINUTES", "min"),
        ("SECONDS", "sec"),
        ("BODY_WEIGHT", "bod"),
    )

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        unique=True,
    )
    name_es = models.CharField(
        verbose_name=_("Name ES"),
        max_length=255,
        blank=False,
        unique=True,
    )
    load_units = models.CharField(verbose_name=_("Load units"), choices=LOAD_UNITS)
    explanation = models.TextField(verbose_name=_("Explanation"), blank=True)
    explanation_es = models.TextField(verbose_name=_("Explanation ES"), blank=True)
    submuscles = models.ManyToManyField(
        SubMuscle,
        related_name="exercise",
        blank=True,
    )
    muscles = models.ManyToManyField(
        Muscle,
        related_name="exercise",
        blank=True,
    )
    muscular_group = models.ManyToManyField(
        MuscularGroup,
        related_name="exercise",
        blank=True,
    )
    image = models.ImageField(verbose_name=_("Image"), blank=True, null=True)
    image_url = models.URLField(verbose_name=_("Image URL"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name",]

class TrainingSession(models.Model):
    """
    Defines a training sessions with predefined exercises.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        unique=True,
    )

    excercices = models.ManyToManyField(Exercise, related_name="training_session")

    def __str__(self) -> str:
        return self.name


class CustomTrainingSession(TrainingSession):
    """
    Training Session with the exercises selected by the user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_training_session",
    )


class TrainingSessionRecord(models.Model):
    """
    Registers a training session
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="training_exercise_record",
    )
    date = models.DateField(verbose_name=_("Date"), default=now, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"


class ExerciseRecord(models.Model):
    """
    Used to record an Exercise
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="exercise_record",
    )
    date = models.DateField(verbose_name=_("Date"), default=now, blank=True)
    exercise = models.ForeignKey(
        Exercise,
        verbose_name=_("Exercise"),
        on_delete=models.CASCADE,
        related_name="exercise_record",
    )
    repetitions = models.PositiveIntegerField(verbose_name=_("Repetitions"))
    load = models.PositiveIntegerField(verbose_name=_("Load"))

    training_session = models.ForeignKey(
        TrainingSessionRecord,
        on_delete=models.CASCADE,
        related_name="exercise_record",
    )

    def __str__(self) -> str:
        return f"{self.exercise} - {self.date}: {self.load} {self.exercise.load_units} x {self.repetitions}"  # noqa: E501

    class Meta:
        ordering = ["exercise__name", "date"]