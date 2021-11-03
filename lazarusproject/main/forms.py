from .models import Table, US_SIZES, CURRENCY_CHOICES, Meetings
from django import forms
from django.forms import ModelForm, DateInput, NumberInput, Select, TextInput, PasswordInput, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class TableForm(ModelForm):
    extra = forms.IntegerField(required=True,initial='1', min_value=1, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Кол-во'
    }))

    class Meta:
        model = Table
        fields = ["userID", "title", "size", "currencyprice", "currencybuy", "currencysell", "currencysellprice", "anyprice", "datebuy", "datesell", "notes"]
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
            "currencyprice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Price'
            }),
            "currencybuy": Select(choices=CURRENCY_CHOICES, attrs={
                'class': 'form-select form-select-sm',
                'placeholder': 'Model Currency'
            }),
            "currencysell": Select(choices=CURRENCY_CHOICES, attrs={
                'class': 'form-select form-select-sm ',
                'placeholder': 'Model Currency'
            }),
            "currencysellprice": NumberInput(attrs={
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
            "notes": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Заметки',
                'rows': '1'
            }),
        }


class MeetingForm(ModelForm):
    class Meta:
        model = Meetings
        fields = ['title', 'datemeeting', 'sellprice', 'notes']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name'
            }),
            "sellprice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Sell Price'
            }),
            "datemeeting": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата встречи',
                'type': 'date'
            }),
            "notes": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заметки'
            }),
        }


class AddItemForMeetingForm(ModelForm):

    itemsellprice = forms.DecimalField(required=True, initial='0', min_value=0, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Кол-во'}))

    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('username')
        super(AddItemForMeetingForm, self).__init__(*args, **kwargs)
        self.fields['meet'].queryset = Meetings.objects.filter(userID=self.username)
        self.fields['meet'].empty_label = None

    class Meta:
        model = Table
        fields = ['meet', 'itemsellprice']
        widgets = {
            "meet": Select(attrs={
                'class': 'form-select',
                'aria-label': '.form-select-lg example',
            })}



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
