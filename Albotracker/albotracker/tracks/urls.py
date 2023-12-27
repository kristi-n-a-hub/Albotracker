from django.urls import path
from . import views

urlpatterns = [
    # Отслеживаем все, что после /tracks/
    path("", views.tracks_home, name="tracks_home")
]
