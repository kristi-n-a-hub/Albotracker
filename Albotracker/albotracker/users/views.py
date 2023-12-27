from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserChangeFormFreeAccess
from django.contrib.auth import logout


def users_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users_profile')  # Замените 'home' на имя вашего URL-шаблона для главной страницы
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'users/users_login.html', context)


def users_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()

            login(request, user)
            # После этого перенаправляем пользователя на главную страницу
            return redirect('users_profile')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'users/users_signup.html', context)


def users_logout(request):
    logout(request)
    return redirect('users_login')


@login_required
def users_profile(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserChangeFormFreeAccess(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_profile')
    else:
        form = CustomUserChangeFormFreeAccess(instance=user)

    context = {'form': form}
    return render(request, 'users/users_profile.html', context)
