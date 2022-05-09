from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import CustomUser, StudentsClass


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('student', 'uczeń'), ('teacher', 'nauczyciel')],
                             required=True, label='Rola')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'role')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = self.fields['password1'].help_text = self.fields['password2'].help_text = ''
        self.fields['role'].help_text = 'Wybierz odpowiednią rolę'

        self.fields['username'].label = 'login'
        self.fields['password1'].label = 'haslo'
        self.fields['password2'].label = 'powtórz hasło'
        self.fields['email'].label = 'adres email'


class StudentsClassForm(forms.ModelForm):
    class Meta:
        model = StudentsClass
        fields = '__all__'
        exclude = ['members', 'owner']
