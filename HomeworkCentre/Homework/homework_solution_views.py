from typing import List
from django.utils import timezone
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from .models import Homework, HomeworkSolution, HomeworkSolutionRating, Homework
from .homework_solution_forms import HomeworkSolutionForm, HomeworkSolutionRatingForm


class HomeworkSolutionCreateView(LoginRequiredMixin, CreateView):
    '''
    Widok tworzący odpowiedź do zadania
    '''
    model = HomeworkSolution
    form_class = HomeworkSolutionForm
    template_name = 'homework_templates/add_solution.html'
    success_url = '/homework/'
    login_url = '/user/login/'
    

    def get_initial(self):
        if HomeworkSolution.objects.filter(homework_id=self.kwargs['pk'], student=self.request.user).exists():
            raise Http404('ODPOWIEDŹ DO ZADANIA JUŻ ISTNIEJE')

        homework = get_object_or_404(Homework, pk=self.kwargs['pk'])
        if homework.deadline <= timezone.now():
            raise Http404('CZAS NA ODPOWIEDŹ JUŻ MINĄŁ')

        self.initial.update({
            'student': self.request.user,
            'homework': homework,
        })
        return super(HomeworkSolutionCreateView, self).get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.initial['homework']
        context['desc'] = self.initial['homework'].description
        return context

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class HomeworkSolutionListView(LoginRequiredMixin, ListView):
    model = HomeworkSolution
    context_object_name = 'solution_list'
    template_name = 'homework_templates/solutions.html'
    login_url = '/user/login/'
    # permission_required = 'Homework.add_homework_solution_rating'

    def get_queryset(self):
        '''
        Zwraca wszystkie (albo przypisane do konkretnego zadania) odpowiedzi, które są przypisane do zadań danego nauczyciela
        REFACTOR: --- które nie mają jeszcze oceny
        '''

        homework = self.kwargs.get('id') or None

        if not homework:
            return HomeworkSolution.objects.filter(homework__in=self.request.user.teacher.all(), solution_rated=None)

        return HomeworkSolution.objects.filter(homework=homework, solution_rated=None)


class HomeworkSolutionRatingCreateView(PermissionRequiredMixin, CreateView):
    model = HomeworkSolutionRating
    form_class = HomeworkSolutionRatingForm
    template_name = 'homework_templates/add_rating.html'
    success_url = '/homework/solution/'
    login_url = '/user/login/'
    permission_required = 'Homework.add_homeworksolutionrating'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solution_to_rate'] = get_object_or_404(
            HomeworkSolution, id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.rated_by = self.request.user
        form.instance.solution = self.get_context_data()['solution_to_rate']
        return super().form_valid(form)


class HomeworkSolutionRatingListView(LoginRequiredMixin, ListView):
    '''
    Lista ocen :
    a) wszystkich wystawionych przez nauczyciela
        a1) do konkretnego zadania
    b) otrzymanych z perspektywy studenta
    '''
    model = HomeworkSolutionRating
    context_object_name = 'rating_list'
    template_name = 'homework_templates/teacher_ratings.html'
    login_url = '/user/login/'

    def get_queryset(self):
        user_groups = self.request.user.groups.values_list(
            'name', flat=True)

        if 'Teachers' in user_groups:
            if self.kwargs.get('homework_id'):
                solutions = HomeworkSolution.objects.filter(
                    homework_id=self.kwargs.get('homework_id'))
                ratings = HomeworkSolutionRating.objects.filter(
                    rated_by=self.request.user)
                print(solutions)
                return ratings.filter(solution__in=solutions)
            
            return self.request.user.rated_by.all()

        elif 'Students' in user_groups:
            self.template_name = 'homework_templates/student_ratings.html'
            return HomeworkSolutionRating.objects.filter(solution__in=self.request.user.student.all()).order_by('-date_added')

class HomeworkSolutionRatingDetailView(LoginRequiredMixin, DetailView):
    model = HomeworkSolutionRating
    template_name = 'homework_templates/rating.html'
    context_object_name = 'rate'
    login_url = '/user/login/'
