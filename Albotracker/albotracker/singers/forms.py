from django import forms
from .models import Genre
from .models import Singer


class GenreFilterForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 2}),  # Установите нужное значение для 'size'
        required=False
    )
    # genres = forms.ModelMultipleChoiceField(
    #     queryset=Genre.objects.all(),
    #     widget=forms.CheckboxSelectMultiple(attrs={'class': 'genre-checkbox'}),
    #     required=False,
    # )


class AddSingerForm(forms.ModelForm):
    class Meta:
        model = Singer
        fields = ['alias', 'photo', 'genres']

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        # Проверяем, уникален ли псевдоним
        if Singer.objects.filter(alias=alias).exists():
            raise forms.ValidationError('Исполнитель с таким псевдонимом уже есть в базе данных.')
        return alias
