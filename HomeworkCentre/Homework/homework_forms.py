from django import forms
from django.http import request
from django.contrib.admin import widgets as admin_widgets
from .models import Homework
from User.models import StudentsClass


class HomeworkForm(forms.ModelForm):
    temp_deadline = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(date_attrs={'placeholder': 'Wybierz date', 'class': 'datepicker'},
                                                                              time_attrs={'placeholder': 'Ustaw godzinę', 'class': 'timepicker'}))

    class Meta:
        model = Homework
        fields = ['title', 'description',
                  'available_formats', 'temp_deadline', 'students']

    def clean(self):
        self.instance.deadline = self.cleaned_data.get('temp_deadline')
        return super().clean()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(HomeworkForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Tytuł'
        self.fields['description'].label = 'Opis'
        self.fields['available_formats'].label = 'Format załączników'
        self.fields['temp_deadline'].label = 'Termin oddania'
        self.fields['students'].label = 'Grupy studentów'
        self.fields['students'].widget.attrs['class'] = 'orange-text text-darken-4'
        self.fields['students'].queryset = user.owner.all()
        # self.fields['students'].queryset = StudentsClass.objects.all()
