from django.shortcuts import render
from .models import Track
from singers.models import Genre
from singers.forms import GenreFilterForm


def tracks_home(request):
    form = GenreFilterForm(request.GET)
    tracks = Track.objects.all()

    if form.is_valid():
        genres = form.cleaned_data['genres']
        if genres:
            tracks = tracks.filter(genres__in=genres)

    context = {
        'tracks': tracks,
        'form': form
    }
    return render(request, 'tracks/tracks_home.html', context)
    # form = GenreFilterForm(request.GET)
    #
    # # Обработка формы
    # if form.is_valid():
    #     selected_genres = form.cleaned_data['genres']
    #     singers_queryset = Singer.objects.all()
    #
    #     # Фильтрация по выбранным жанрам
    #     for genre in selected_genres:
    #         singers_queryset = singers_queryset.filter(genres=genre)
    #
    #     # Отправка отфильтрованных исполнителей в шаблон
    #     context = {'singers': singers_queryset, 'form': form}
    #     return render(request, 'singers/singers_home.html', context)
    #
    # # Если форма не отправлена, отобразите ее с пустыми результатами
    # context = {'singers': [], 'form': form}
    # return render(request, 'singers/singers_home.html', context)
