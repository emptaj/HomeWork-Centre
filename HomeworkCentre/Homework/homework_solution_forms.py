from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets
from django.http import request
from .models import HomeworkSolution, Homework, HomeworkSolutionRating


class HomeworkSolutionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSolution
        fields = ['description', 'homework', 'homework_file']

    def __init__(self, *args, **kwargs):
        super(HomeworkSolutionForm, self).__init__(*args, **kwargs)
        self.fields['homework_file'].label = 'załącznik'
        self.fields['description'].label = 'Odpowiedź/komentarz'
    def clean(self):
        print(self.cleaned_data)
        desc = self.cleaned_data['description']
        file = self.cleaned_data['homework_file']
        if not desc and not file:
            raise ValidationError('odpowiedź nie może być pusta')

        data = self.cleaned_data['homework_file']
        if data:
            homework_format = str(data).rsplit('.', 1)[1]
            if homework_format not in self.cleaned_data['homework'].available_formats:
                raise ValidationError('Nieprawidłowy format pliku')


class HomeworkSolutionRatingForm(forms.ModelForm):
    class Meta:
        model = HomeworkSolutionRating
        fields = ('rating', 'feedback', )
        RATES = ((1, 1),
                 (2, 2),
                 (3, 3),
                 (4, 4),
                 (5, 5))
        widgets = {
            'rating': widgets.Select(choices=RATES),
        }

    def __init__(self, *args, **kwargs):
        super(HomeworkSolutionRatingForm, self).__init__(*args, **kwargs)
        self.fields['feedback'].label = 'Komentarz'
        self.fields['rating'].label = 'Ocena'

