from django.contrib import admin
from .models import Homework, HomeworkSolution, HomeworkSolutionRating
# Register your models here.

admin.site.register(Homework)
admin.site.register(HomeworkSolution)
admin.site.register(HomeworkSolutionRating)