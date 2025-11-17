from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    isu = forms.CharField(
        max_length=6,
        required=True,
        label='Номер ИСУ'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'isu', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'student'
        user.is_superuser = False
        user.is_staff = False
        
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите ваш пароль'})
    )