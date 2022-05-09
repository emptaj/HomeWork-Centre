from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password, role='student', **other_fields):
        if not email:
            raise ValueError('Users must have an email_address')
        if not first_name or not last_name:
            raise ValueError('Users must have first and last name')

        user = self.model(username=username, first_name=first_name, last_name=last_name, email=self.normalize_email(email),
                          **other_fields
                          )
        user.set_password(password)
        user.save()

        if role == 'student':
            user.groups.add(Group.objects.get(name='Students'))

        elif role == 'teacher':
            user.groups.add(Group.objects.get(name='Teachers'))

        user.is_active = False
        return user

    def create_superuser(self, username, first_name, last_name, email, password, **other_fields):
        user = self.create_user(username, first_name,
                                last_name, email, password, 'teacher')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    first_name = models.CharField(null=False, blank=False, max_length=150)
    last_name = models.CharField(null=False, blank=False, max_length=150)
    email = models.EmailField(blank=False, unique=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class StudentsClass(models.Model):
    name = models.CharField(blank=False, null=False,
                            max_length=100, unique=True)
    description = models.CharField(null=False, blank=False, max_length=100)
    members = models.ManyToManyField(
        CustomUser, limit_choices_to={'groups__name': "Students"}, related_name='members', blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Teachers"}, related_name='owner')
    
    def __str__(self):
        return f'{self.name} | WŁAŚCICIEL : {self.owner}'
