from .models import Table, US_SIZES
from django import forms
from django.forms import ModelForm, DateInput, NumberInput, Select, TextInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = ["userID", "title", "size", "price", "sellprice", "anyprice", "datebuy", "datesell", "notes"]
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


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NickName'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


