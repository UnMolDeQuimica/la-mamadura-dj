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
    load_units = models.CharField(verbose_name=_("Load units"), choices=LOAD_UNITS)
    description = models.TextField(verbose_name=_("Description"), blank=True)
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
        ordering = [
            "name",
        ]


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
    load = models.FloatField(verbose_name=_("Load"))

    training_session = models.ForeignKey(
        TrainingSessionRecord,
        verbose_name=_("Training Session"),
        on_delete=models.CASCADE,
        related_name="exercise_record",
    )

    notes = models.TextField(verbose_name=_("Notes"), blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.exercise} - {self.date}: {self.load} {self.exercise.load_units} x {self.repetitions}"  # noqa: E501

    class Meta:
        ordering = ["exercise__name", "date"]


class TrainingSessionTemplate(models.Model):
    """
    Defines a training sessions with predefined exercises.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        unique=True,
    )

    exercises = models.ManyToManyField(
        Exercise, related_name="training_session_template", through="ExerciseTemplate"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="training_session_template",
        blank=True,
        null=True,
    )
    notes = models.TextField(verbose_name=_("Notes"), blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class ExerciseTemplate(models.Model):
    template = models.ForeignKey(
        TrainingSessionTemplate,
        on_delete=models.CASCADE,
        verbose_name=_("Training Session template"),
        related_name="exercise_template",
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        verbose_name=_("Exercise"),
        related_name="exercise_template",
    )
    sets = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Sets"))

    def __str__(self):
        return f"{self.sets} x {self.exercise.name} - {self.template.name}"

    class Meta:
        ordering = ["template__name"]


class Weight(models.Model):
    weight = models.FloatField(
        verbose_name=_("Weight"), default=0, blank=True, null=True
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="weight"
    )
    date = models.DateField(verbose_name=_("Date"), default=now, blank=True)

    def __str__(self):
        return f"{self.weight} kg"

    class Meta:
        ordering = ["date"]
