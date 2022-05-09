from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('classes/', views.StudentClassListView.as_view(), name='classes'),
    path('classes/<int:class_id>/members', views.StudentClassMembersListView.as_view(), name='class_members'),
    path('classes/available', views.StudentClassListView.as_view(available=True), name='classes_available'),
    path('classes/create', views.CreateStudentsClass.as_view(), name='class_create'),
    path('classes/join/<int:pk>', views.join_to_class, name='class_join'),
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.CustomLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(next_page='user:user_login'), name='user_logout'),
]

app_name = 'User'
