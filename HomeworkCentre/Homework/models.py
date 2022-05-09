from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from User.models import CustomUser, StudentsClass
from multiselectfield import MultiSelectField

# Create your models here.


class Homework(models.Model):
    # NEED REFACTOR
    AVAILABLE_FORMATS = (('pdf', 'pdf'),
                         ('doc', 'doc'),
                         ('docx', 'docx'),
                         ('txt', 'txt'),
                         ('py', 'py'),
                         ('cpp', 'cpp'),
                         ('mp3', 'mp3'),
                         ('jpg', 'jpg'),
                         ('png', 'png'),
                         ('zip', 'zip'),
                         ('rar', 'rar'),
                         ('tar.gz', 'tar.gz'))
    title = models.CharField(blank=False, null=False,
                             unique=True, max_length=250)
    description = models.TextField(blank=True, null=True, max_length=500)
    available_formats = MultiSelectField(
        choices=AVAILABLE_FORMATS, null=False, blank=False)
    deadline = models.DateTimeField(
        auto_now_add=False, blank=False, null=False)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={
                                'groups__name': "Teachers"}, related_name='teacher')
    students = models.ManyToManyField(
        StudentsClass, related_name='students')

    def __str__(self):
        return f'{self.title}'


class HomeworkSolution(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name='homework')
    homework_file = models.FileField(
        upload_to=f'homework_solutions/', null=False, blank=True, )
    description = models.TextField(blank=True, null=True, max_length=320)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  limit_choices_to={
        'groups__name': "Students"}, related_name='student')
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        homework_name = self.homework.title
        return f'{homework_name} - {self.student}'


class HomeworkSolutionRating(models.Model):
    rating = models.PositiveIntegerField(null=False, blank=False, validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])

    feedback = models.CharField(null=True, blank=True, max_length=300)
    solution = models.OneToOneField(
        HomeworkSolution, on_delete=models.CASCADE, related_name='solution_rated')
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={
        'groups__name': "Teachers"}, related_name='rated_by'
    )

    date_added = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.solution} | {self.rated_by} | {self.date_added}'

