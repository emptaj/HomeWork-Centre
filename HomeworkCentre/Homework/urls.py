from . import homework_views
from .import homework_solution_views
from django.urls import path

urlpatterns = [
    path('', homework_views.HomeworkList.as_view(), name='homeworks'),
    path('<int:class_id>', homework_views.HomeworkList.as_view(), name='homeworks_for_class'),
    path('create/', homework_views.HomeworkFormView.as_view(),
         name='create_homework'),
    path('solution/create/<int:pk>', homework_solution_views.HomeworkSolutionCreateView.as_view(),
         name='create_solution'),
    path('solution/', homework_solution_views.HomeworkSolutionListView.as_view(),
         name='solutions'),
    path('<int:id>/solution', homework_solution_views.HomeworkSolutionListView.as_view(),
         name='solutions_to_homework'),
    path('solution/<int:pk>/rate', homework_solution_views.HomeworkSolutionRatingCreateView.as_view(),
         name='rating_create'),
    path('rating/', homework_solution_views.HomeworkSolutionRatingListView.as_view(),
         name='ratings'),
    path('<int:homework_id>/rating', homework_solution_views.HomeworkSolutionRatingListView.as_view(),
         name='ratings_to_homework'),
    path('rating/<int:pk>', homework_solution_views.HomeworkSolutionRatingDetailView.as_view(),
         name='rating'),

]

app_name = 'Homework'
