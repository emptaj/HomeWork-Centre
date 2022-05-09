from django.shortcuts import render
from django.views.generic import CreateView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import HomeworkSolution, Homework, HomeworkSolutionRating
from .homework_forms import HomeworkForm
import datetime

# Create your views here.

class HomeworkList(LoginRequiredMixin, ListView):
    '''
    Zwraca listę zadań:
    a) przypisanych do zalogowanego nauczyciela
    b) przypisanych do zalogowanego ucznia
    '''
    model = Homework
    context_object_name = 'homework_list'
    template_name = 'homework_templates/student_homeworks.html'
    login_url = '/user/login/'

    def get_queryset(self):
        user_groups = self.request.user.groups.values_list(
            'name', flat=True)
        if 'Teachers' in user_groups:
            self.template_name = 'homework_templates/teacher_homeworks.html'
            if self.kwargs.get('class_id'):
                return self.request.user.teacher.all().filter(students=self.kwargs.get('class_id'))
            return self.request.user.teacher.all()

        if 'Students' in user_groups:
            if self.kwargs.get('class_id'):
                print(self.kwargs.get('class_id'))
                student_homeworks = Homework.objects.filter(students=self.kwargs.get('class_id'),
                                                            deadline__gt=datetime.datetime.now()).distinct()
            else:
                student_homeworks = Homework.objects.filter(students__in=self.request.user.members.all(),
                                                            deadline__gt=datetime.datetime.now()).distinct()

            student_solutions = self.request.user.student.all()
            homework_without_solution = [exercise for exercise in student_homeworks
                                         if not any(item in exercise.homework.all() for item in student_solutions)]
            print(homework_without_solution)
            return homework_without_solution


class HomeworkFormView(PermissionRequiredMixin, CreateView):
    '''
    Widok służy do tworzenia zadań
    '''
    form_class = HomeworkForm
    template_name = 'homework_templates/add_homework.html'
    success_url = '/homework/'
    login_url = '/user/login/'
    permission_required = 'Homework.add_homework'

    def __init__(self, **kwargs):
        print('tworze widok')
        super().__init__(**kwargs)

    def form_valid(self, form):
        print('prosze dzialaj')
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(HomeworkFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

