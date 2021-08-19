from .models import Table, US_SIZES
from django import forms
from django.forms import ModelForm, DateInput, NumberInput, Select, TextInput, PasswordInput
from django.contrib.auth.models import User


class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = ["title", "size", "price", "sellprice", "anyprice", "datebuy", "datesell", "notes"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Name'
            }),
            "size": Select(choices=US_SIZES, attrs={
                'class': 'form-select',
                'aria-label': '.form-select-lg example',
                'placeholder': 'Model Size'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Price'
            }),
            "sellprice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Sell Price'
            }),
            "anyprice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Доп расходы'
            }),
            "datebuy": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата покупки',
                'type': 'date'
            }),
            "datesell": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата продажи',
                'type': 'date'
            }),
            "notes": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заметки'
            }),
        }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Login'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }

    def clean(self):
        usermane = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(usermane=usermane).exists():
            raise forms.ValidationError(f'Пользователь с логином {usermane} не найден')
        user = User.objects.filter(usermane=usermane).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data


