from django import forms
from .models import Album
from .models import Single
from tracks.models import Track


class AddAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'release_year', 'cover', 'tracks']

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     return title


class AddTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'release_year', 'cover', 'audio', 'genres', 'singers']


class AddSingleForm(forms.ModelForm):
    class Meta:
        model = Single
        fields = ['track']
