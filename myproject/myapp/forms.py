from django.forms import ModelForm, TextInput
from .models import Movie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Movie Name'}),
        }
