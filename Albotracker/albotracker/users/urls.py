from django.urls import path
from . import views

urlpatterns = [
    # Отслеживаем все, что после /users/
    # path("", LoginView.as_view(template_name='users/users_login.html'), name="users_login"),
    path("", views.users_login, name="users_login"),
    path("profile", views.users_profile, name="users_profile"),
    path("signup", views.users_signup, name="users_signup"),
    path("logout", views.users_logout, name='users_logout'),
]