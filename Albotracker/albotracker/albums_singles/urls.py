from django.urls import path
from . import views

urlpatterns = [
    # Отслеживаем все, что после /singers/
    path("", views.albums_singles_home, name="albums_singles_home"),
    path("add_album", views.add_album, name="add_album"),
    path('add_track/', views.add_track, name='add_track'),
    path("add_single", views.add_single, name="add_single"),
    path("album/<int:pk>", views.AlbumView.as_view(), name="album_view"),
    path("single/<int:pk>", views.SingleView.as_view(), name="single_view")
]
