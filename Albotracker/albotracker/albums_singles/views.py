from django.shortcuts import render
from .models import Album
from .models import Single
from singers.models import Singer
from django.shortcuts import render, redirect
from .forms import AddAlbumForm
from .forms import AddTrackForm
from django.http import JsonResponse
from .forms import AddSingleForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test


def is_moderator(user):
    return user.groups.filter(name='moderator').exists()


def albums_singles_home(request):
    albums = Album.objects.all()
    singles = Single.objects.all()

    for album in albums:
        # Получение всех исполнителей для альбома
        singers_in_album = Singer.objects.filter(tracks__in=album.tracks.all()).distinct()
        # Добавление списка исполнителей к каждому альбому в словаре
        album.singers_in_album = singers_in_album

    for single in singles:
        # Получение всех исполнителей для альбома
        singers_in_single = single.track.singers.all()
        # Добавление списка исполнителей к каждому альбому в словаре
        single.singers_in_single = singers_in_single

    context = {
        'albums': albums,
        'singles': singles
    }
    return render(request, 'albums_singles/albums_singles_home.html', context)


class SingleView(DetailView):
    model = Single
    template_name = 'albums_singles/single_view.html'
    context_object_name = 'single'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем объект альбома
        single = context['single']

        # Получаем всех исполнителей сингла
        singers = single.track.singers.all()

        track = single.track

        context['singers'] = singers
        context['track'] = track
        return context


class AlbumView(DetailView):
    model = Album
    template_name = 'albums_singles/album_view.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем объект альбома
        album = context['album']

        # Получаем всех исполнителей альбома (исполнителей всех треков альбома)
        singers = album.tracks.values_list('singers', flat=True)

        # Убираем дубликаты исполнителей
        unique_singers = Singer.objects.filter(pk__in=set(singers))

        tracks = album.tracks.all()

        context['singers'] = unique_singers
        context['tracks'] = tracks
        return context


@user_passes_test(is_moderator, login_url='albums_singles_home')
def add_album(request):
    if request.method == 'POST':
        form = AddAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем альбом в базе данных
            album = form.save(commit=False)  # commit=False, чтобы избежать мгновенного сохранения

            tracks = form.cleaned_data.get('tracks', [])

            album.save()

            album.tracks.set(tracks)

            return redirect('albums_singles_home')  # Перенаправление на страницу с альбомами или другую страницу
    else:
        form = AddAlbumForm()

    track_form = AddTrackForm(request.POST, request.FILES)
    context = {
        'form': form,
        'track_form': track_form
    }
    return render(request, 'albums_singles/add_album.html', context)


@user_passes_test(is_moderator, login_url='albums_singles_home')
def add_track(request):
    if request.method == 'POST':
        form = AddTrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)

            # Обработка выбранных жанров и исполнителей
            genres = form.cleaned_data.get('genres', [])
            singers = form.cleaned_data.get('singers', [])

            # Сохранение трека
            track.save()

            # Добавление выбранных жанров и исполнителей к треку
            track.genres.set(genres)
            track.singers.set(singers)

            return JsonResponse({'success': True})
    else:
        form = AddTrackForm()

    context = {'track_form': form}
    return render(request, 'albums_singles/add_album.html', context)


@user_passes_test(is_moderator, login_url='albums_singles_home')
def add_single(request):
    if request.method == 'POST':
        form = AddSingleForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем сингл в базе данных
            form.save()

            return redirect('albums_singles_home')  # Перенаправление на страницу с альбомами или другую страницу
    else:
        form = AddSingleForm()

    track_form = AddTrackForm(request.POST, request.FILES)
    context = {
        'form': form,
        'track_form': track_form
    }
    return render(request, 'albums_singles/add_single.html', context)
