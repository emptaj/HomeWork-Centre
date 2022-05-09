from typing import List
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from .forms import StudentsClassForm, CustomUserCreationForm
from .models import CustomUser, StudentsClass
from django.views.generic import CreateView, ListView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
import datetime
from Homework.models import HomeworkSolutionRating, Homework, HomeworkSolution
# Create your views here.

class StudentClassMembersListView(PermissionRequiredMixin, ListView):
    permission_required = 'user.add_studentsclass'
    login_url = '/user/login'
    template_name = 'user_templates/teacher_class_members.html'
    context_object_name = 'members'
    model = CustomUser

    def get_queryset(self):
        return StudentsClass.objects.get(id=self.kwargs['class_id']).members.all()

class StudentClassListView(LoginRequiredMixin, ListView):
    '''
    Widok zwraca wszystkie klasy:
    a) do których przypisano zalogowanego studenta
        a1) do których można dołączyć
    b) które stworzył zalogowany nauczyciel
    '''
    model = StudentsClass
    context_object_name = 'class_list'
    template_name = 'user_templates/teacher_classes.html'
    login_url = '/user/login/'

    available = False
    
    def get_queryset(self):
       
        #wszystkie przypisane klasy (ze strony studenta)
        user_groups = self.request.user.groups.values_list('name', flat=True)
        if 'Teachers' in user_groups:
            return self.request.user.owner.all()

        if 'Students' in user_groups and not self.available:
            self.template_name = 'user_templates/student_classes.html'
            return self.request.user.members.all()

        elif 'Students' in user_groups and self.available:
            classes = self.request.user.members.all()
            self.template_name = 'user_templates/available_classes.html'
            return StudentsClass.objects.exclude(members=self.request.user)


class CreateStudentsClass(PermissionRequiredMixin, CreateView):
    '''
    Widok tworzący klasę studentów (dla nauczyciela)
    '''
    permission_required = 'User.add_studentsclass'
    form_class = StudentsClassForm
    template_name = 'user_templates/add_students_class.html'
    success_url = '/user/'
    login_url = '/user/login/'


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = 'user_templates/register.html'
    form_class = CustomUserCreationForm
    success_url = '/homework/'
    

    def form_valid(self, form):
        #NAJPIERW TRZEBA STWORZYC USERA Z COMMIT=FALSE (UTWORZY, ALE NIE ZAPISZE)
        user_group = Group.objects.get(
            name='Students') if form.cleaned_data['role'] == 'student' else Group.objects.get(name='Teachers')
        user = form.save(commit=False)
        user.is_active = False
        user.is_staff = False
        user.is_admin = False
        user.save()
        user.groups.add(user_group)
        return super().form_valid(form)


def join_to_class(request, pk):
    class_to_join = get_object_or_404(StudentsClass, id=pk)
    class_to_join.members.add(request.user)
    return redirect('User:classes_available')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'user_templates/student_main.html'
    login_url = '/user/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_groups = self.request.user.groups.values_list(
            'name', flat=True)
        
        if 'Students' in user_groups:
            context['rating_list'] = HomeworkSolutionRating.objects.filter(
                solution__in=self.request.user.student.all()).order_by('-date_added')[:4]

            student_homeworks = Homework.objects.filter(students__in=self.request.user.members.all(),
                                                        deadline__gt=datetime.datetime.now()).distinct()

            student_solutions = self.request.user.student.all()
            homework_without_solution = [exercise for exercise in student_homeworks
                                        if not any(item in exercise.homework.all() for item in student_solutions)]
            
            context['homework_list'] = homework_without_solution[:4]

        if 'Teachers' in user_groups:
            self.template_name = 'user_templates/teacher_main.html'
            context['solution_list'] = HomeworkSolution.objects.filter(
                homework__in=self.request.user.teacher.all(), solution_rated=None).order_by('-date_added')[:3]
            context['rating_list'] = self.request.user.rated_by.all().order_by('-date_added')[:3]
            context['homework_list'] = self.request.user.teacher.all()[:3] # poprawic sortowanie: dodac date_added do modelu homework
            
        return context


class CustomLoginView(LoginView):
    template_name = 'user_templates/login.html'
    redirect_authenticated_user = True


    def get_success_url(self):
        return reverse_lazy('user:home')

