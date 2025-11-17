from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

@login_required
def dashboard_view(request):
    student_data = None
    
    from django.db import connection

    if request.method == 'POST' and 'show_student_data' in request.POST:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT "Сезон", "Название соревнования", "Уровень соревнования", "Достоинство награды", "Дистанция", "Детали" as "Класс судна", "Финишный протокол" FROM "Личные достижения за сезон" WHERE "ИСУ спортсмена"={request.user.isu}')
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                student_data = {
                    'columns': columns,
                    'rows': rows
                }
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
    
    context = {
        'user': request.user,
        'student_data': student_data
    }
    return render(request, 'accounts/dashboard.html', context)