from django.shortcuts import render
from .models import Singer, Genre
from .forms import GenreFilterForm
from django.shortcuts import render, redirect
from .forms import AddSingerForm
from django.views.generic import DetailView
from albums_singles.models import Single
from albums_singles.models import Album
from django.contrib.auth.decorators import user_passes_test


def singers_home(request):
    form = GenreFilterForm(request.GET)
    singers = Singer.objects.all()

    if form.is_valid():
        genres = form.cleaned_data['genres']
        if genres:
            singers = singers.filter(genres__in=genres)

    context = {
        'singers': singers,
        'form': form
    }
    return render(request, 'singers/singers_home.html', context)
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


class SingerView(DetailView):
    model = Singer
    template_name = 'singers/singer_view.html'
    context_object_name = 'singer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        albums = Album.objects.filter(tracks__singers=self.object).distinct()

        for album in albums:
            # Получение всех исполнителей для альбома
            singers_in_album = Singer.objects.filter(tracks__in=album.tracks.all()).distinct()
            # Добавление списка исполнителей к каждому альбому в словаре
            album.singers_in_album = singers_in_album

        singles = Single.objects.filter(track__singers=self.object).distinct()

        for single in singles:
            # Получение всех исполнителей для альбома
            singers_in_single = single.track.singers.all()
            # Добавление списка исполнителей к каждому альбому в словаре
            single.singers_in_single = singers_in_single

        context['singles'] = singles
        context['albums'] = albums
        # context['albums'] = Album.objects.filter(tracks__singers=self.object)
        return context


def is_moderator(user):
    return user.groups.filter(name='moderator').exists()


@user_passes_test(is_moderator, login_url='singers_home')
def add_singer(request):
    if request.method == 'POST':
        form = AddSingerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('singers_home')
    else:
        form = AddSingerForm()

    genres = Genre.objects.all()

    context = {
        'form': form,
        'genres': genres
    }
    return render(request, 'singers/add_singer.html', context)

