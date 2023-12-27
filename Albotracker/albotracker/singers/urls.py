from django.urls import path
from . import views

urlpatterns = [
    # Отслеживаем все, что после /singers/
    path("", views.singers_home, name="singers_home"),
    path("add_singer", views.add_singer, name="add_singer"),
    path("<int:pk>", views.SingerView.as_view(), name="singer_view")
]